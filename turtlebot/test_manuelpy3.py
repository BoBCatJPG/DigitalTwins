import struct
import threading
from threading import Lock
from turtle import *
from distance_control import *
from polar_control import *
import socket

speed_lock = Lock()
target_lock = Lock()

def send_data(position, sock):
    packed_data = struct.pack('fff', position[0], 19, position[1])  # y fittizia
    sock.sendto(packed_data, ("192.168.70.106", 9002))
    # print("invio", position[0], 0, position[1])

def receive_data(sock, t, p):
    while True:
        data, addr = sock.recvfrom(1024)
        packed_data = struct.unpack('fffff', data)

        godot_x = packed_data[0]
        godot_y = packed_data[1]
        godot_z = packed_data[2]
        velocity = packed_data[3]
        flag = packed_data[4]

        if flag == 1:
            t.setSpeeds(0, 0)
            t.setPose(godot_x, godot_z, 0)
            print("pose: ", t.getPose().x, t.getPose().y, t.getPose().theta)
        else:
            p.change_vel_max(velocity)
            print("Ricevo:", godot_x, godot_y, godot_z, velocity, flag)
            p.setTarget(godot_x, godot_z)

if __name__ == "__main__":
    t = Turtlebot()
    t.open()
    t.setPose(160, 160, 0)
    t.setSpeeds(0, 0)

    p = PolarController(t,
                        160.0,  # wheel base
                        0.005,  # 5ms
                        5,  # kp
                        150,  # saturation
                        5,  # kp ang
                        50,  # saturation ang
                        10)  # tolerance
    p.start()

    HOST = "192.168.70.109"  # Indirizzo IP del robot digitale
    PORT = 9001  # Porta utilizzata per ricevere

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    # Crea un thread separato per la ricezione dei dati dal robot digitale
    receive_thread = threading.Thread(target=receive_data, args=(sock, t, p))
    receive_thread.daemon = True  # Il thread terminerà quando il programma principale termina
    receive_thread.start()

    try:
        while True:
            position = [t.getPose().x, t.getPose().y]
            send_data(position, sock)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        sock.close()
