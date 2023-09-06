# -*- coding: utf-8 -*-
from turtle import *
from distance_control import *
from polar_control import *
import socket
import struct

def send_data(position, sock):
    packed_data = struct.pack('fff', position[0], 20, position[1])  # y fittizia
    sock.sendto(packed_data, ("192.168.70.106", 9002))
    print("Invio:", position[0], 20, position[1])

if __name__ == "__main__":
    # Inizializza il Turtlebot e il suo controllore
    t = Turtlebot()
    t.open()
    t.setPose(0, 0, 0)
    t.setSpeeds(0,0)
    
    p = PolarController(t,
                        160.0,  # wheel base
                        0.005,  # 5ms
                        5,  # kp
                        150,  # saturation
                        5,  # kp ang
                        50,  # saturation ang
                        10)  # tolerance
    p.start()
    
    # Imposta i parametri per la connessione al robot digitale
    HOST = "192.168.70.109"  # Indirizzo IP del robot digitale
    PORT = 9001  # Porta utilizzata per ricevere
    
    # Crea un socket UDP per la comunicazione con il robot digitale
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))

    try:
        while True:
            # Ricevi i dati dal robot digitale
            data, addr = sock.recvfrom(1024)
            packed_data = struct.unpack('fff', data)
            
            # Adatta le coordinate del Turtlebot reale al sistema di riferimento di Godot
            godot_x = packed_data[0]
            godot_y = packed_data[1]
            godot_z = packed_data[2]
            
            print("Ricevo:", godot_x, godot_y, godot_z) 
            # Aggiorna la posizione e la velocità del Turtlebot reale utilizzando il Polar Controller
            p.setTarget(godot_x, godot_z)
            
            # Controlla se il Turtlebot reale ha raggiunto la posizione target

            pose = t.getPose()
            position = [t.getPose().x, t.getPose().y]
            send_data(position, sock)
            
        
            

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        sock.close()
