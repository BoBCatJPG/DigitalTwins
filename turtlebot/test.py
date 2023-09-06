#
# position_control_task.py
#
import sys
from turtle import *
from distance_control import *
from polar_control import *

if __name__ == "__main__":

    t = Turtlebot()
    t.open()
    t.setPose(0, 0, 0)

    d = None
    
    #d = DistanceController(t,
    #                       0.005, # 5ms
    #                       5,   # kp
    #                       200)  # saturation
    #d.start()

    p = PolarController(t,
                        160.0, # wheel base
                        0.005, # 5ms
                        5,   # kp
                        150, # saturation
                        5,  # kp ang
                        50,  # saturation ang
                        10 ) # tolerance
    p.start()

    while True:
        cmd_string = raw_input("Command> ")
        commands = cmd_string.split()
        if commands == []:
            continue
        
        if commands[0] == "help":
            print("Commands:")
            print("quit          exit the program")
            print("pose          return the pose of the robot")
            print("pset x y th   set the pose of the robot")
            print("speed l r     set the speed of left and right wheels")
            print("stop          stop the robot")
            
        elif commands[0] == "pose":
            print(t.getPose())
            
        elif commands[0] == "quit":
            if d is not None:
                d.stop()
            if p is not None:
                p.stop()
            sys.exit(0)
            
        elif commands[0] == "speed":
            print(t.setSpeeds(int(commands[1]), int(commands[2])))
            
        elif commands[0] == "stop":
            print(t.setSpeeds(0,0))
            
        elif commands[0] == "pset":
            print(t.setPose(int(commands[1]), int(commands[2]), int(commands[3])))
            
        elif commands[0] == "clear":
            t.clearDistances()
            print("ok")
            
        elif commands[0] == "fwd":
            if d is not None:
                d.setTarget(int(commands[1]))
            
        elif commands[0] == "go":
            p.setTarget(int(commands[1]),int(commands[2]))
            
        else:
            print("Invalid command")
