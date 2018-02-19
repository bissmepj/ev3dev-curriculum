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

    def Rescue(self):
        ev3.Sound.speak('Rescue the Hostage').wait()


    def shutdown(self):
        robot.shutdown2()
def main():
    robot = robo.Snatch3r()
    ev3.Sound.speak('Spec Ops Robot Online')
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc('mosquitto.csse.rose-hulman.edu', 10)
    dc = DataContainer()
    robot.loop_forever()

    remote1 = ev3.RemoteControl(channel=1)
    remote2 = ev3.RemoteControl(channel=2)
    remote3 = ev3.RemoteControl(channel=3)

    remote1.on_red_up = lambda state: handle_move_red_up(state, robot)
    remote1.on_red_down = lambda state: handle_move_red_down(state, robot)

    remote1.on_blue_up = lambda state: handle_move_blue_up(state, robot)
    remote1.on_blue_down = lambda state: handle_move_blue_down(state, robot)

    remote2.on_red_up = lambda state: arm_up(state, robot)
    remote2.on_red_down = lambda state: arm_down(state, robot)

    remote3.on_red_up = lambda state: beacon_seek(state, robot)

    btn = ev3.Button()

    while dc.running:
        btn.process()
        remote1.process()
        remote2.process()
        time.sleep(0.01)

    btn.on_up = lambda state: handle_button_press(state, mqtt_client, "Hostage Rescued")

    def handle_move_red_up(state, robot):
        if state:
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
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
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
            robot.right_motor.run_forever(speed_sp=-600)
        else:
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
            robot.right_motor.stop(stop_action='brake')

    def beacon_seek(state, robot):
        if state:
            robot.beacon_seeker(1, 300, 100)

    def arm_up(state, robot):
        if state:
            robot.arm_up()

    def arm_down(state, robot):
        if state:
            robot.arm_down()


    def handle_button_press(button_state, mqtt_client, button_name):
        if button_state:
            print('Hostage has been rescued')
            mqtt_client.send_message('rescued', [button_name])




# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()