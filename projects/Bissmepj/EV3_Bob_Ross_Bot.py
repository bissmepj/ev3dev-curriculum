"""
The idea behind this project is that the robot acts as a paint brush for a tkinter GUI.
This includes the ability to lift up or put down the paint brush and to select colors.
Quit button on Robot, arrow keys to move, u and j to lift arm
"""

import robot_controller as robo
import time
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3


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

    def quit(self):
        self.robot.running = False
        self.robot.left_motor.stop(stop_action='brake')
        self.robot.right_motor.stop(stop_action='brake')

        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)

        print('Goodbye')
        ev3.Sound.speak('Goodbye').wait()


def main():
    robot = robo.Snatch3r()
    delegate = MyDelegate(robot)
    mqtt_client = com.MqttClient(delegate)
    mqtt_client.connect_to_pc()
    time.sleep(3)
    print("I'm Ready")

    btn = ev3.Button()
    btn.on_up = lambda state: color_change(mqtt_client, robot)
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IPaddress of a GCP broker

    while True:
        btn.process()
        time.sleep(.1)


def color_change(client, robot):
    color = robot.color_sensor.color
    if color == ev3.ColorSensor.COLOR_BLACK:
        color = "black"
    elif color == ev3.ColorSensor.COLOR_BLUE:
        color = "blue"
    elif color == ev3.ColorSensor.COLOR_GREEN:
        color = "green"
    elif color == ev3.ColorSensor.COLOR_YELLOW:
        color = "yellow"
    elif color == ev3.ColorSensor.COLOR_RED:
        color = "red"
    else:
        color = "black"

    client.send_message("color_change", [color])


main()
