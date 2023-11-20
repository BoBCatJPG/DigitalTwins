import struct
import threading
from threading import Lock
from turtle3 import *
from distance_control import *
from polar_control3 import *
import socket
import time
from lds_diver import *
lidar = LidarLDS(port="/dev/ttyUSB0", baudrate=230400, timeout=1000)
GODOT_HOST = "192.168.70.121"
exit_event = threading.Event()


def send_data(position, sock):
    packed_data = struct.pack(
        'fff', position[0], position[1], position[2])  # y fittizia
    sock.sendto(packed_data, (GODOT_HOST, 9002))
    # print("invio: ",position[0],position[1])


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
            t.setPose(godot_x, godot_z, godot_y)
            print("pose: ", t.getPose().x, t.getPose().y, t.getPose().theta)
        elif flag == 2:
            print("chiusura forzata")
            exit_event.set()

        else:
            p.change_vel_max(velocity)
            p.setTarget(godot_x, godot_z)
            # print("Ricevo:", godot_x, godot_y, godot_z, velocity, flag)


def lidar_data_thread():
    while not exit_event.is_set():
        ranges, intensities, scan_time, rpms = lidar.get_scan_data()

        # Invia i dati del LIDAR al robot digitale su Godot
        send_lidar_data(ranges, intensities, scan_time, rpms)


def send_lidar_data(ranges, intensities, scan_time, rpms):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Converte i dati in un formato adeguato per l'invio
    packed_data = struct.pack('360f', *ranges)
    sock.sendto(packed_data, (GODOT_HOST, 9003))


if __name__ == "__main__":
    t = Turtlebot()
    t.open()
    t.setPose(600, 534, 0)
    t.getPose()
    print("hello")
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

    lidar.stop_scan()
    time.sleep(1)
    lidar.start_scan()

    HOST = "192.168.70.123"  # Indirizzo IP del turtlebot
    PORT = 9001  # Porta utilizzata per ricevere
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    data, info = sock.recvfrom(1024)  # aggiunta 14 nov 11:12
    print("connected to ", info[0])
    GODOT_HOST = info[0]

    # Crea un thread separato per la ricezione dei dati dal robot digitale
    receive_thread = threading.Thread(target=receive_data, args=(sock, t, p))
    # Il thread terminerà quando il programma principale termina
    receive_thread.daemon = True
    receive_thread.start()

    # Crea un thread separato per la ricezione dei dati del LIDAR
    lidar_thread = threading.Thread(target=lidar_data_thread)
    # Il thread terminerà quando il programma principale termina
    lidar_thread.daemon = True
    lidar_thread.start()

    try:
        while not exit_event.is_set():
            position = [t.getPose().x, t.getPose().y, t.getPose().theta]
            send_data(position, sock)
            # Aggiungi un piccolo ritardo per limitare l'invio dei dati
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        exit_event.set()
        sock.close()
        lidar.stop_scan()
