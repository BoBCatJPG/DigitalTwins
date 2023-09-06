#
#
#

import serial, struct, time, sys

MODE_SINGLE = 0
MODE_MULTIPLE = 1

def wait_char(p, c):
    while True:
        b = p.read(1)
        print(hex(ord(b)))
        if b is None:
            raise "timeout"
        if ord(b[0]) == c:
            return


def get_response(p):
    wait_char(p, 0xa5)
    wait_char(p, 0x5a)
    resp = p.read(5)
    if resp is None:
        raise "timeout"

    resp = struct.unpack("<Lc", resp)
    (leng, mode, typ) =  (resp[0] & 0x3fffffff, resp[0] >> 30, resp[1])
    return (leng, mode, typ)


def get_single_response(p):
    (leng, mode, typ) = get_response(p)
    if mode == MODE_SINGLE:
        return p.read(leng)
    else:
        raise "multiple response in requesting single response"


def get_multiple_response(p):
    (leng, mode, typ) = get_response(p)
    if mode == MODE_MULTIPLE:
        return leng
    else:
        raise "single response in requesting multiple response"

def get_scan_data(p,l):
    data = p.read(l)
    scan_data = struct.unpack("<chh")
    quality = scan_data[0] >> 2
    s = (scan_data[0] & 2) >> 1
    not_s = scan_data[0] & 1
    check = scan_data[1] & 1
    angle = scan_data[1] >> 1
    distance = scan_data[2]
    return (quality, s, not_s, check, angle, distance)


def get_acc_board(p):
    p.write("\xa5\xff")
    return get_single_response(p)


def get_info(p):
    p.write("\xa5\x50")
    return get_single_response(p)

def get_healt(p):
    p.write("\xa5\x52")
    return get_single_response(p)


def stop_scan(p):
    p.write("\xa5\x25")


def start_scan(p):
    p.write("\xa5\x20")
    return get_multiple_response(p)


def set_motor_pwm(p,pwm):
    arg = struct.pack("<h", pwm)
    packet = "\xa5\xf0\x02" + arg
    cks = 0
    for c in packet:
        print(hex(ord(c)))
        cks = cks ^ ord(c)
    print(hex(cks))
    p.write(arg + chr(cks))
    return get_single_response(p)


if __name__ == "__main__":
    port = serial.Serial (port = "/dev/ttyUSB0", baudrate = 115200, timeout = 1000)
    print("GET INFO", get_info(port))
    print( "STOP", stop_scan(port))
    #print "GET ACC", get_acc_board(port)
    print("PWM", set_motor_pwm(port, 660))
    l = start_scan(port)
    print( "START SCAN", l)
    while True:
        print(get_scan_data(port, l))




