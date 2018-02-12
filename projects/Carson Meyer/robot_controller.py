"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method clled arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    def __init__(self):  # Initializes the Robot and it's components
        self.left_led = ev3.Leds.LEFT
        self.right_led = ev3.Leds.RIGHT
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.running = False
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.beacon_seeker = ev3.BeaconSeeker()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        assert self.pixy
        assert self.ir_sensor
        assert self.color_sensor
        assert self.left_motor
        assert self.right_motor
        assert self.left_motor

    def drive_inches(self, dist, speed):  # Drives a given distance and speed, determined by the user.

        position = dist * 90

        self.left_motor.run_to_rel_pos(position_sp=position, speed_sp=speed, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp=position, speed_sp=speed, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees, speed):  # Turns robot by given degrees at given speed

        degrees = degrees * 4.6

        self.left_motor.run_to_rel_pos(position_sp=degrees, speed_sp=speed, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp=-degrees, speed_sp=speed, stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_down(self):  # Returns arm to down position from up position.
        max_speed = 900
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=max_speed)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

    def arm_up(self):  # Moves arm upwards, this causes the Snatch3r to grab whatever is in front of it.
        max_speed = 900
        self.arm_motor.run_forever(speed_sp=max_speed)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')
        ev3.Sound.beep()

    def arm_calibration(self):  # Calibrates the arm by moving it up to it's limit
        # and then sends it down the determined distance for its 0 point.
        max_speed = 900
        self.arm_motor.run_forever(speed_sp=max_speed)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')
        ev3.Sound.beep()

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def shutdown(self, dc):  # Stops robot and breaks it out of its forever loop.
        dc.running = False
        self.running = False
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)

        print('Goodbye')
        ev3.Sound.speak('Goodbye').wait()

    def loop_forever(self):  # Sets the robot in an infinite loop of actions.
        self.running = True
        while self.running:
            time.sleep(.01)

    def forward(self, left_speed, right_speed):  # Drives forward at given speeds until told to stop.
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def backward(self, left_speed, right_speed):  # Drives backward at given speeds until told to stop.
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def left(self, left_speed, right_speed):  # Turns the robot left at given speeds until told to stop or move.
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def right(self, left_speed, right_speed):  # Turns the robot right at the given speeds until told to stop.
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def stop(self):  # Stops the robot.
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def shutdown2(self):  # Shuts down the robot when in an infinite loop and breaks the loop.
        self.running = False
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

        ev3.Sound.speak('Goodbye')
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)

    def seek_beacon(self, channel, forward_speed, turn_speed):  # Using the IR sensor, tracks and picks-up the beacon.
        self.beacon_seeker = ev3.BeaconSeeker(channel=channel)
        while not self.touch_sensor.is_pressed:
            # The touch sensor can be used to abort the attempt (sometimes handy during testing)

            # DONE: 3. Use the beacon_seeker object to get the current heading and distance.
            current_heading = self.beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = self.beacon_seeker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:

                if math.fabs(current_heading) < 2:
                    if current_distance == 1:
                        time.sleep(1)
                        self.stop()
                        return True
                    if current_distance > 1:
                        print("On the right heading. Distance: ", current_distance)
                        self.forward(forward_speed, forward_speed)
                if math.fabs(current_heading) > 2 and math.fabs(current_heading) < 10:
                    if current_heading < 0:
                        self.left(turn_speed, turn_speed)
                        print("Adjusting heading: ", current_heading)
                    if current_heading > 0:
                        self.right(turn_speed, turn_speed)
                        print("Adjusting heading: ", current_heading)
                if math.fabs(current_heading) > 10:
                    self.right(turn_speed, turn_speed)
                    print("Heading is too far off to fix: ", current_heading)

            time.sleep(0.2)
        # The touch_sensor was pressed to abort the attempt if this code runs.
        print("Abandon ship!")
        self.stop()
        return False
