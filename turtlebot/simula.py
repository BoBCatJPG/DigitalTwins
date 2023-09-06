import time
import struct
import socket

HOST = '127.0.0.1'
PORT = 9001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

turtlebot_position = (0.0, 0.0, 0.0)
is_moving = False

def receive_data():
    global turtlebot_position, is_moving
    packed_data, _ = sock.recvfrom(12)
    turtlebot_position = struct.unpack('fff', packed_data)
    print("Received from Godot:", turtlebot_position)
    is_moving = True

def move_turtlebot_to_target(target):
    global turtlebot_position, is_moving
    is_moving = True
    
    step_size = 0.002  # Definisci il passo di interpolazione
    
    #while True:  # Continua finché non raggiungi la soglia
    dx = target[0] - turtlebot_position[0]
    dz = target[2] - turtlebot_position[2]
    
    # Calcola la posizione intermedia
    intermediate_position = (
        turtlebot_position[0] + dx * step_size,
        turtlebot_position[1],
        turtlebot_position[2] + dz * step_size
    )
    
    # Invia la posizione intermedia a Godot
    send_data(intermediate_position)
    
    # Aggiorna la posizione corrente del Turtlebot
    turtlebot_position = intermediate_position
    
    # Calcola la distanza rimanente
    distance = abs(turtlebot_position[0] - target[0]) + abs(turtlebot_position[2] - target[2])
    
    # Controlla se la distanza è inferiore alla soglia minima
    #if distance < 0.01:
       # break
    
    time.sleep(1)  # Attendi un secondo
        
    is_moving = False


def send_data(position):
    packed_data = struct.pack('fff', position[0], position[1], position[2])
    sock.sendto(packed_data, (HOST, 9002))
    print("Sent:", position)

if __name__ == "__main__":
    try:
        sock.bind((HOST, PORT))

        while True:
            #if not is_moving:
            receive_data()

            move_turtlebot_to_target(turtlebot_position)

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        sock.close()
