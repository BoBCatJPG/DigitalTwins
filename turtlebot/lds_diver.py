#
#
#

import serial, struct, time, sys, math


class LidarLDS :

    def __init__(self, port = "/dev/ttyUSB0", baudrate = 230400, timeout = 1000) -> None:
        self.p = port = serial.Serial (port = port, baudrate = baudrate, timeout = timeout)
        self.angle_increment = (2.0*math.pi/360.0)
        self.angle_min = 0.0
        self.angle_max = 2.0*math.pi-self.angle_increment
        self.range_min = 0.12
        self.range_max = 3.5
        self.ranges = [-1] * 360
        self.intensities = [-1] * 360
        self.motor_speed = 0
        self.good_sets = 0
        self.index = 0

    def wait_char(self, c):
        while True:
            b = self.p.read(1)
            if b is None:
                raise "timeout"
            b = bytearray(b)
            if b[0] == c:
                return

    def stop_scan(self):
        self.p.write(b'e')


    def start_scan(self):
        self.p.write(b'b')


    def get_scan_data(self):
        self.wait_char(0xfa)
        self.wait_char(0xa0)

        rpms = 0
       
        raw_bytes =  bytearray(bytes([0xfa, 0xa0]) + self.p.read(2518))
        # copiare da https://github.com/ROBOTIS-GIT/hls_lfcd_lds_driver/blob/master/src/hlds_laser_publisher.cpp

        if raw_bytes[0] == 0xFA and raw_bytes[1] == 0xA0:

            for i in range(0, len(raw_bytes), 42):
                if raw_bytes[i] == 0xFA and raw_bytes[i+1] == (0xA0 + i / 42):
                    self.good_sets+=1
                    self.motor_speed += (raw_bytes[i+3] << 8) + raw_bytes[i+2]; 

                    for j in range(i+4, i+40, 6):
                        self.index = int(6*(i/42) + (j-4-i)/6)
                        byte0 = raw_bytes[j]
                        byte1 = raw_bytes[j+1]
                        byte2 = raw_bytes[j+2]
                        byte3 = raw_bytes[j+3]
                        intensity = (byte1 << 8) + byte0
                        _range = (byte3 << 8) + byte2

                        self.ranges[359-self.index] = _range / 1000.0
                        self.intensities[359-self.index] = intensity
            
            rpms= self.motor_speed / self.good_sets / 10
            self.time_increment = (float)(1.0 / (rpms*6))
            self.scan_time = self.time_increment * 360
                  
        
        return (self.ranges, self.intensities, self.scan_time, rpms)



if __name__ == "__main__":

    try:
        lidar = LidarLDS(port = "/dev/ttyUSB0", baudrate = 230400, timeout = 1000)
        print("STOP", lidar.stop_scan())
        time.sleep(1)
        print("START", lidar.start_scan())
        while True:
            ranges, intensities, scan_time, rpms = lidar.get_scan_data()
            i = 0
            print(i, ranges[i], "metri", intensities[i])
    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        lidar.stop_scan()

