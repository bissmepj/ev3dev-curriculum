"""
The idea behind this project is that the robot acts as a paint brush for a tkinter GUI.
This includes the ability to lift up or put down the paint brush and to select colors.
Quit button on Robot, arrow keys to move, u and j to lift arm
"""

import time
import ev3dev.ev3 as ev3
import robot_controller as robo
import mqtt_remote_method_calls as com


class MyDelegate(object):

    def __init__(self, robot):
        self.running = True
        self.color = "Black"
        self.robot = robot

    def turn_left(self):
        self.robot.turn_degrees(90, 100)


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.

