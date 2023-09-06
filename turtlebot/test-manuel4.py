# -*- coding: utf-8 -*-
import sys
import socket
import signal
from threading import Thread
from Queue import Queue
from turtle import *
from distance_control import *
from polar_control import *

def process_data(data):
    # Interpretazione dei dati ricevuti dal pacchetto UDP
    data = data.strip().decode()
    if data.startswith("vel"):
        vel_data = data.split(" ")
        vel_x = float(vel_data[1])
        vel_y = float(vel_data[2])
        vel_ang = float(vel_data[3])
        # Aggiornamento della velocità del TurtleBot con i valori ricevuti
        t.setSpeeds(vel_x, vel_y)
        t.setAngularSpeed(vel_ang)
    elif data.startswith("pos"):
        pos_data = data.split(" ")
        pos_x = float(pos_data[1])
        pos_y = float(pos_data[2])
        pos_ang = float(pos_data[3])
        # Aggiornamento della posizione del TurtleBot con i valori ricevuti
        t.setPose(pos_x, pos_y, pos_ang)
    else:
        print("Dati non validi:", data)

def receive_commands(server_socket, command_queue):
    while True:
        data, _ = server_socket.recvfrom(1024)
        command_queue.put(data)

def process_commands(command_queue):
    while True:
        data = command_queue.get()
        process_data(data)
        command_queue.task_done()
def signal_handler(signal,frame):
    print("programma terminato")
    sys.exit(0)

if __name__ == "__main__":
    t = Turtlebot()
    t.open()
    t.setPose(0, 0, 0)

    d = None
    p = None
    
    d = DistanceController(t, 0.005, 5, 200)
    d.start()

    p = PolarController(t, 160.0, 0.005, 5, 150, 5, 50, 10)
    p.start()

    # Inizializzazione e impostazione del socket UDP
    server_address = ('192.168.1.3', 9001)  # Inserisci l'indirizzo IP e la porta corrispondenti al tuo TurtleBot reale
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(server_address)

    # Coda per i comandi in arrivo
    command_queue = Queue()

    # Avvio dei thread per la ricezione e l'elaborazione dei comandi
    receive_thread =threading.Thread(target=receive_commands, args=(server_socket, command_queue))
    receive_thread.daemon = True
    receive_thread.start()

    process_thread =threading.Thread(target=process_commands, args=(command_queue,))
    process_thread.daemon = True
    process_thread.start()


    signal.signal(signal.SIGINT, signal_handler)
    while True:
        pass
