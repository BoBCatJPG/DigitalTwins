#
# turtle.py
#
import serial
import struct
import threading

class Pose:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.theta = 0
        self.vl = 0 # velocita' ruota sinistra (attuale)
        self.vr = 0 # veloctia' ruota destra (attuale)
        self.v = 0 # velocita' lineare del robot
        self.w = 0 # velocita' angolare del robot
        self.linear = 0 # distanza lineare percorsa dal robot
        self.angular = 0 # distanza angolare percorsa dal robot

    def __repr__(self):
        return "(%f, %f, %f) [%f, %f] [%f, %f] [%f, %f]" % \
          (self.x, self.y, self.theta, self.vl, self.vr, self.v, self.w, self.linear, self.angular)


class Turtlebot:

    def __init__(self, port='/dev/ttyACM0', baud=115200):
        self.__p = port
        self.__b = baud
        self.__pose = Pose()
        self.mutex = threading.Lock()
        self.w_max=2.84#aggiunta manuel 21 Jun

    def open(self):
        self.__ser = serial.Serial(self.__p, self.__b, 8, "N", 1, 1000)

    def __decode_nibble(self, s):
        if (s >= 0x30)and(s <= 0x39):
             return s - 0x30
        elif (s >=0x41)and(s <= 0x46):
            return s - 0x41 + 10
        else:
            return -1;

    def __decode_hex(self, s1, s2):
        s1 = self.__decode_nibble(s1)
        s2 = self.__decode_nibble(s2)
        if (s1 == -1)or(s2 == -1):
            return -1
        else:
            return (s1 << 4) | s2

    def __decode_packet(self, s):
        i = 1
        packet = []
        while i < len(s):
            if s[i] == b'>'[0]:
                break
            ch = self.__decode_hex(s[i], s[i+1])
            #print hex(ch),
            if ch == -1:
                return None
            packet.append(ch)
            i = i + 2
        #print ""
        return packet

    def __encode_hex(self, c):
        c1 = c >> 4
        c2 = c & 0xf
        if c1 > 9:
            c1 = chr(0x41 - 10 + c1)
        else:
            c1 = chr(0x30 + c1)
        if c2 > 9:
            c2 = chr(0x41 - 10 + c2)
        else:
            c2 = chr(0x30 + c2)
        return c1 + c2

    def __encode_packet(self, s):
        packet = ""
        for c in s:
            if isinstance(c, int):
                packet = packet + self.__encode_hex(c)
            else:
                packet = packet + self.__encode_hex(ord(c))
        return packet

    def __transaction(self, packet):
        self.mutex.acquire()
        try:
            packet_bytes = bytes('#' + packet + '$', 'utf-8')
            self.__ser.write(packet_bytes)
            while True:
                line = self.__ser.readline()
                #print(line)
                if (line is None) or (len(line) == 0):
                    return None
                if (line[0] == b'<'[0]):  # and(line[-1] == '>'):
                    decoded_packet = self.__decode_packet(line)
                    return (decoded_packet[0], decoded_packet[1], decoded_packet[2:])
        finally:
            self.mutex.release()

    def getPose(self):
        reply = self.__transaction("01")
        if reply is not None:
            reply_bytes = reply[2]  # Convert the string to bytes
            if len(reply_bytes) == 36:
                d = struct.unpack("<fffffffff", bytes(reply_bytes))
                self.__pose.x = d[0]
                self.__pose.y = d[1]
                self.__pose.theta = d[2]
                self.__pose.vl = d[3]
                self.__pose.vr = d[4]
                self.__pose.v = d[5]
                self.__pose.w = d[6]
                self.__pose.linear = d[7]
                self.__pose.angular = d[8]
            else:
                print("Received data has incorrect length:", len(reply_bytes))

        return self.__pose



    def setSpeeds(self, vl, vr):
        data = struct.pack("<ii", int(vl),int(vr))
        return self.__transaction("02" + self.__encode_packet(data))

    def setPose(self, x, y, t):
        data = struct.pack("<iii", int(x), int(y), int(t))
        return self.__transaction("03" + self.__encode_packet(data))

    def clearDistances(self):
        return self.__transaction("04")
        
