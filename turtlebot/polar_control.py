# -*- coding: utf-8 -*-

from __future__ import print_function
import threading
import time
import math

class PolarController(threading.Thread):

    def __init__(self, turtle_if, wb, delta_t, kp_lin, sat_lin, kp_angular, sat_angular, tolerance):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.mutex = threading.Lock()
        self.wheel_base = wb
        self.kp_lin = kp_lin        
        self.sat_lin = sat_lin
        self.kp_angular = kp_angular
        self.sat_angular = sat_angular
        self.robot = turtle_if
        self.delta_t = delta_t
        p = self.robot.getPose()
        self.target_pos = (p.x, p.y)
        self.distance_tolerance = tolerance
      
    def change_vel_max(self,velocity):
      self.sat_lin=velocity
      

    def setTarget(self, x, y):
        self.mutex.acquire()
        self.target_pos = (x, y)
        self.mutex.release()

    def start(self):
        self.isRunning = True
        threading.Thread.start(self)

    def stop(self):
        self.isRunning = False
        
    def run(self):
        while self.isRunning:
            time.sleep(self.delta_t)

            self.mutex.acquire()
            p = self.robot.getPose()

            (target_x, target_y) = self.target_pos
               
            dx = target_x - p.x
            dy = target_y - p.y
        
            target_heading = math.atan2(dy, dx)
            distance = math.hypot(dx, dy)

            heading_error = self.normalize_angle(target_heading - p.theta)
            direction = 1

            if abs(heading_error) > (math.pi/2):
                  direction = -1; # the point is on the back of the robot
                  heading_error = self.normalize_angle(heading_error + math.pi)
    
            v = self.kp_lin * distance
            w = self.kp_angular * heading_error

            if v > self.sat_lin:
               v = self.sat_lin
            elif v < -self.sat_lin:
               v = - self.sat_lin
               
            if w > self.sat_angular:
               w = self.sat_angular
            elif w < -self.sat_angular:
               w = - self.sat_angular

            vl = direction * v - (w * self.wheel_base / 2)
            vr = direction * v + (w * self.wheel_base / 2)

            if abs(distance) < self.distance_tolerance:
               vl = 0
               vr = 0    
            
            self.mutex.release()
            self.robot.setSpeeds(vl, vr)
            

            
    def normalize_angle(self,a):
       if a > math.pi:
          return a - math.pi*2
       if a < -math.pi:
          return a + math.pi*2
       else:
          return a
