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
        self.arm_state = 0

    def turn_left(self):
        degrees = 90 * 4.6

        self.robot.left_motor.run_to_rel_pos(position_sp=-degrees, speed_sp=100, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.robot.right_motor.run_to_rel_pos(position_sp=degrees, speed_sp=100, stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.robot.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_right(self):
        degrees = 90 * 4.6

        self.robot.left_motor.run_to_rel_pos(position_sp=degrees, speed_sp=200, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.robot.right_motor.run_to_rel_pos(position_sp=-degrees, speed_sp=200, stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.robot.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def forward(self):
        degrees = 360

        self.robot.left_motor.run_to_rel_pos(position_sp=degrees, speed_sp=200, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.robot.right_motor.run_to_rel_pos(position_sp=degrees, speed_sp=200,
                                              stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.robot.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm(self):
        if self.arm_state == 0:
            self.robot.arm_up()
            self.arm_state = 1
        else:
            self.robot.arm_down()
            self.arm_state = 0


def main():
    robot = robo.Snatch3r()
    delegate = MyDelegate(robot)
    mqtt_client = com.MqttClient(delegate)
    mqtt_client.connect_to_pc()
    time.sleep(3)
    print("I'm Ready")
    btn = ev3.Button
    btn.on_up = lambda state: color_change(mqtt_client, ev3.ColorSensor.color)
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IPaddress of a GCP broker
    while True:
        btn.process()
        time.sleep(.1)


def color_change(client, color):
    client.send_message("color_change", [color])


main()
