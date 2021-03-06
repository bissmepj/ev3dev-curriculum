#!/usr/bin/env python3
"""
The goal of this module to combine using the Pixy with the drive motors.  You will track a color using the Pixy and turn
the robot so that it is always facing the color signature.  You will need to teach Pixy a color before starting to
implement the code, then make the robot always face the color as you move it around.  The robot will only spin and never
move forwards or backwards.

Authors: David Fisher and Nathaniel Huey.
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.

import time

import ev3dev.ev3 as ev3
import robot_controller as robo


def main():
    print("--------------------------------------------")
    print(" Color tracking")
    print("--------------------------------------------")
    ev3.Sound.speak("Color tracking").wait()
    print("Press the touch sensor to exit this program.")

    # This code assumes you have setup the pixy object on the Snatch3r class.
    # Add the pixy property to that class if you have not done so already.
    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    turn_speed = 100

    while not robot.touch_sensor.is_pressed:


        x = robot.pixy.value(1)
        y = robot.pixy.value(2)
        print("(X, Y)= ({}, {})".format(x, y))

        if x < 150:
            robot.left(turn_speed, turn_speed)
        elif x > 170:
            robot.right(turn_speed, turn_speed)
        elif x > 150 and x < 170:
            robot.stop()



        time.sleep(0.25)
    robot.stop()
    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()

# TODO: 4. Call over a TA or instructor to sign your team's checkoff sheet.
#
# Observations you should make, the Pixy cam could potentially be used for a lot of cool project ideas, but if you
# decide to use the Pixy you should be aware of what it does well and what it doesn't do well.


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
