import sys
import socket
from turtle import *
from distance_control import *
from polar_control import *
import threading
from Queue import Queue


def receive_commands(server_socket, command_queue, exit_flag):
    try:
        while not exit_flag.is_set():
            data = server_socket.recvfrom(1024)
            elemento = data[0]
            tuple_str = str(elemento)
            index = tuple_str.find("COMANDO:")
            commands = tuple_str[index + 8:]
            commands = commands.split('\x00')
            commands = commands[0].split(' ')
            print(data)
            print(commands)

            if commands:
                command_queue.put(commands)
    except KeyboardInterrupt:
        server_socket.close()


if __name__ == "__main__":
    t = Turtlebot()
    t.open()
    t.setPose(0, 0, 0)

    d = None
    p = PolarController(t,
                        160.0,  # wheel base
                        0.005,  # 5ms
                        5,  # kp
                        150,  # saturation
                        5,  # kp ang
                        50,  # saturation ang
                        10)  # tolerance
    p.start()

    server_address = ('192.168.1.2', 9001)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(server_address)

    command_queue = Queue()
    exit_flag = threading.Event()

    cmd_string = raw_input("Select mode S:(socket) C(cmd)> ").strip().lower()

    receive_thread = threading.Thread(target=receive_commands, args=(server_socket, command_queue, exit_flag))
    receive_thread.start()

    try:
        while not exit_flag.is_set():
            if cmd_string == 's':
                # Ricevi i comandi dalla coda
                if not command_queue.empty():
                    commands = command_queue.get()
                else:
                    continue
            elif cmd_string == 'c':
                comd = raw_input("Command> ")
                commands = comd.split()

            if not commands:
                continue

            if commands[0] == "help":
                print("Commands:")
                print("quit          exit the program")
                print("pose          return the pose of the robot")
                print("pset x y th   set the pose of the robot")
                print("speed l r     set the speed of left and right wheels")
                print("stop          stop the robot")
                print("go x y        set destination of the robot")
                print("clear         clear the distances")
                print("fwd dist      move forward by a specified distance")

            elif commands[0] == "pose":
                print(t.getPose())

            elif commands[0] == "quit":
                if d is not None:
                    d.stop()
                if p is not None:
                    p.stop()
                exit_flag.set()

            elif commands[0] == "speed":
                if len(commands) >= 3:
                    print(t.setSpeeds(int(commands[1]), int(commands[2])))
                else:
                    print("Invalid command")

            elif commands[0] == "stop":
                print(t.setSpeeds(0, 0))

            elif commands[0] == "pset":
                if len(commands) >= 4:
                    print(t.setPose(int(commands[1]), int(commands[2]), int(commands[3])))
                else:
                    print("Invalid command")

            elif commands[0] == "clear":
                t.clearDistances()
                print("ok")

            elif commands[0] == "go":
                if len(commands) >= 3:
                    print(t.goTo(int(commands[1]), int(commands[2])))
                else:
                    print("Invalid command")

            elif commands[0] == "fwd":
                if len(commands) >= 2:
                    print(t.moveForward(float(commands[1])))
                else:
                    print("Invalid command")

    except KeyboardInterrupt:
        server_socket.close()
