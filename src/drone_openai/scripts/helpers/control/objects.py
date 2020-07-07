#! /usr/bin/env python

import numpy as np
import rospy
import time
import numpy as np
from math import *
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
fpv = [320, 480] #320 half of width

HFOV = 86
DFOV = 98.77


>>>>>>> 50bcf1d0e1655ba5732897e7f7c6b40ad9d4fcbd
class Control:
    def __init__(self):
        self.goal = 0.0  # [angle]
        self.ctrl_c = False
        self._pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self._move_msg = Twist()
        self._pub_takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
        self._takeoff_msg = Empty()
        self._pub_land = rospy.Publisher('/drone/land', Empty, queue_size=1)
        self._land_msg = Empty()

    def stop(self):
        rospy.loginfo("Stopping...")
        self._move_msg.linear.x = 0.0
        self._move_msg.angular.z = 0.0
        self._pub_cmd_vel.publish(self._move_msg)

    def takeoff(self):
        rospy.loginfo('Taking off...')
        i=0
        while not i == 3:
            self._pub_takeoff.publish(self._takeoff_msg)
            time.sleep(1)
            i += 1
    
    def land(self):
        rospy.loginfo('Landing...')
        i=0
        while not i == 3:
            self._pub_land.publish(self._land_msg)
            time.sleep(1)
            i += 1

    def turn(self):
        rospy.loginfo("Turning...")
        self._move_msg.linear.x = 0.0
        self._move_msg.angular.z = 1.0
        self_pub_cmd_vel.publish(self._move_msg)

    def move_forward(self):
        rospy.loginfo("Moving forward...")
        self._move_msg.linear.x = 1.0
        self._move_msg.angular.z = 0.0
        self_pub_cmd_vel.publish(self._move_msg)

    def yaw(self, position):
        #Old
        #f = np.sqrt(640**2+480**2)
        #alpha = DFOV/f
        #new_goal = alpha * float(fpv[0] - position[0])

        #Adaptable angle Latest 
        f = 640.
        alpha = 0.2 * HFOV/f
        new_goal = alpha * float(fpv[0] - position[0])

        yaw = new_goal + self.goal
        self.goal = yaw
        return yaw
