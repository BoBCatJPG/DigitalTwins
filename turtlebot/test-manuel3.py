import sys
import socket
import threading
from turtle import *
from distance_control import *
from polar_control import *

# Funzione per la ricezione dei comandi
def receive_commands(server_socket, command_queue, command_queue_lock):
    while True:
        data = server_socket.recvfrom(1024)
        elemento = data[0]
        tuple_str = str(elemento)
        index = tuple_str.find("COMANDO:")
        commands = tuple_str[index + 8:]
        commands = commands.split('\x00')
        commands = commands[0].split(' ')
        print(data)
        print(commands)
        
        with command_queue_lock:
            command_queue.append(commands)

# Funzione per l'esecuzione dei comandi
def execute_commands(turtlebot, command_queue, command_queue_lock):
    while True:
        with command_queue_lock:
            if command_queue:
                commands = command_queue.pop(0)
        
        if commands:
            if commands[0] == "help":
                print("Commands:")
                print("quit          exit the program")
                print("pose          return the pose of the robot")
                print("pset x y th   set the pose of the robot")
                print("speed l r     set the speed of left and right wheels")
                print("stop          stop the robot")
                print("go x y        set destination of the robot")
                
            elif commands[0] == "pose":
                print(turtlebot.getPose())
                
            elif commands[0] == "quit":
                if d is not None:
                    d.stop()
                if p is not None:
                    p.stop()
                sys.exit(0)
                
            elif commands[0] == "speed":
                print(turtlebot.setSpeeds(int(commands[1]), int(commands[2])))
                
            elif commands[0] == "stop":
                print(turtlebot.setSpeeds(0, 0))
                
            elif commands[0] == "pset":
                print(turtlebot.setPose(int(commands[1]), int(commands[2]), int(commands[3])))
                
            elif commands[0] == "clear":
                turtlebot.clearDistances()
                print("ok")
                
            elif commands[0] == "fwd":
                if d is not None:
                    d.setTarget(int(commands[1]))
                
            elif commands[0] == "go":
                p.setTarget(int(commands[1]), int(commands[2]))
                
            else:
                print("Invalid command")


if __name__ == "__main__":
    t = Turtlebot()
    t.open()
    t.setPose(0, 0, 0)

    d = None

    p = PolarController(t, 160.0, 0.005, 5, 150, 5, 50, 10)
    p.start()

    server_address = ('192.168.1.59', 9001)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(server_address)

    # Crea la coda dei comandi condivisa e il lock per la sincronizzazione
    command_queue = []
    command_queue_lock = threading.Lock()

    # Avvia il thread per la ricezione dei comandi
    receive_thread = threading.Thread(target=receive_commands, args=(server_socket, command_queue, command_queue_lock))
    receive_thread.start()

    # Avvia il thread per l'esecuzione dei comandi
    execute_thread = threading.Thread(target=execute_commands, args=(t, command_queue, command_queue_lock))
    execute_thread.start()

    receive_thread.join()
    execute_thread.join()


        # Assicurati di gestire la terminazione dei thread appropriatamente
