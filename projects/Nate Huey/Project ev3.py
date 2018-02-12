#!/usr/bin/env python3
import mqtt_remote_method_calls as com
import robot_controller as robo

robot = robo.Snatch3r()
class MyDelegate(object):

    def __init__(self):
        self.running = True
    def forward(self, left_speed, right_speed):

        print("Received: {} {}".format(left_speed, right_speed))


        robot.right_motor.run_forever(speed_sp= right_speed)
        robot.left_motor.run_forever(speed_sp=left_speed)
    def backward(self, left_speed, right_speed):

        print("Received: {} {}".format(left_speed, right_speed))

        robot.right_motor.run_forever(speed_sp=-right_speed)
        robot.left_motor.run_forever(speed_sp=-left_speed)

    def right(self, left_speed, right_speed):
        print("Received: {} {}".format(left_speed, right_speed))

        robot.right_motor.run_forever(speed_sp=-right_speed)
        robot.left_motor.run_forever(speed_sp=left_speed)

    def left(self, left_speed, right_speed):
        print("Received: {} {}".format(left_speed, right_speed))

        robot.right_motor.run_forever(speed_sp=right_speed)
        robot.left_motor.run_forever(speed_sp=-left_speed)

    def stop(self):
        robot.right_motor.stop(stop_action='brake')
        robot.left_motor.stop(stop_action='brake')

    def arm_up(self):
        robot.arm_up()

    def arm_down(self):
        robot.arm_down()
    def shutdown(self):
        robot.shutdown2()
def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc('mosquitto.csse.rose-hulman.edu', 10)
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.



# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()