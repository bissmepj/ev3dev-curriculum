#!/usr/bin/env python3
import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3
import time as time

robot = robo.Snatch3r()


class DataContainer(object):
    def __init__(self):
        self.running = True

class MyDelegate(object):

    def __init__(self):
        self.running = True

    def stop(self):
        robot.stop()
        ev3.Leds.LEFT =ev3.Leds.GREEN
        ev3.Leds.RIGHT = ev3.Leds.GREEN

    def perimeter(self):
        white_level = 80
        black_level = 10
        while True:
            if robot.touch_sensor.is_pressed == True:
                break
            if robot.color_sensor.reflected_light_intensity > white_level:
                robot.forward(200, 200)
            if robot.color_sensor.reflected_light_intensity < black_level:
                robot.right(200, 200)
        robot.stop()

    def follow(self):
        robot.pixy.mode = "SIG1"
        turn_speed = 200

        while True:

            x = robot.pixy.value(1)
            y = robot.pixy.value(2)
            print("(X, Y)= ({}, {})".format(x, y))

            if x < 150:
                robot.left(turn_speed, turn_speed)
            elif x > 170:
                robot.right(turn_speed, turn_speed)
            elif x > 150 and x < 170:
                robot.stop()
            if robot.touch_sensor.is_pressed == True:
                break
        robot.stop()
    def seek(self):
        robot.seek_beacon(1, 400, 200)
        robot.arm_up()
        time.sleep(5)
        robot.arm_down()
        time.sleep(5)
        robot.stop()

    def control(self):
        dc = DataContainer()
        remote1 = ev3.RemoteControl(channel=1)
        remote2 = ev3.RemoteControl(channel=2)

        remote1.on_red_up = lambda state: handle_move_red_up(state, robot)
        remote1.on_red_down = lambda state: handle_move_red_down(state, robot)

        remote1.on_blue_up = lambda state: handle_move_blue_up(state, robot)
        remote1.on_blue_down = lambda state: handle_move_blue_down(state, robot)

        remote2.on_red_up = lambda state: handle_arm_up_button(state, robot)
        remote2.on_red_down = lambda state: handle_arm_down_button(state, robot)
        btn = ev3.Button()
        btn.on_backspace = lambda state: handle_shutdown(state, dc)

        while dc.running:
            btn.process()
            remote1.process()
            remote2.process()
            time.sleep(0.01)

        robot.stop()
    def spin(self):
        robot.right(900, 900)
        time.sleep(10)

    def quit(self):
        robot.stop()
        ev3.Sound.speak("Goodbye").wait()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        exit()

def main():
    print("--------------------------------------------")
    print("Fighting Robot")
    print("--------------------------------------------")
    ev3.Sound.speak("Robot Fight Simulator").wait()

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc('mosquitto.csse.rose-hulman.edu', 10)
    robot.loop_forever()

def handle_shutdown(button_state, dc):
    """Exit the program."""
    if button_state:
        dc.running = False

def handle_move_red_up(state, robot):
    if state:
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        robot.left_motor.run_forever(speed_sp=600)
    else:
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
        robot.left_motor.stop(stop_action='brake')

def handle_move_red_down(state, robot):
    if state:
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        robot.left_motor.run_forever(speed_sp=-600)
    else:
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
        robot.left_motor.stop(stop_action='brake')

def handle_move_blue_up(state, robot):
    if state:
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        robot.right_motor.run_forever(speed_sp=600)
    else:
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
        robot.right_motor.stop(stop_action='brake')

def handle_move_blue_down(state, robot):
    if state:
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
        robot.right_motor.run_forever(speed_sp=-600)
    else:
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
        robot.right_motor.stop(stop_action='brake')

def handle_arm_up_button(button_state, robot):
    if button_state:
        robot.arm_up()

def handle_arm_down_button(button_state, robot):
    if button_state:
        robot.arm_down()


main()
