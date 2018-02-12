"""
The idea behind this project is that the robot acts as a paint brush for a tkinter GUI.
This includes the ability to lift up or put down the paint brush and to select colors.
Quit button on Robot, arrow keys to move, u and j to lift arm
"""

import time
import ev3dev.ev3 as ev3
import robot_controller as robo
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class MyDelegate(object):

    def __init__(self, tkinter_frame):
        self.running = True
        self.color = "black"
        self.heading = "north"

    def color_change(self, lego_color):
        if lego_color == ev3.ColorSensor.COLOR_BLACK:
            self.color = "black"
        elif lego_color == ev3.ColorSensor.COLOR_BLUE:
            self.color = "blue"
        elif lego_color == ev3.ColorSensor.COLOR_GREEN:
            self.color = "green"
        elif lego_color == ev3.ColorSensor.COLOR_YELLOW:
            self.color = "yellow"
        elif lego_color == ev3.ColorSensor.COLOR_RED:
            self.color = "red"

    def turn_bot(self, direction):
        if direction == "right":
            if self.heading == "north":
                self.heading = "east"
            elif self.heading == "east":
                self.heading = "south"
            elif self.heading == "south":
                self.heading = "west"
            elif self.heading == "west":
                self.heading = "north"
        else:
            if self.heading == "north":
                self.heading = "west"
            elif self.heading == "west":
                self.heading = "south"
            elif self.heading == "south":
                self.heading = "east"
            elif self.heading == "east":
                self.heading = "north"


def main():
    root = tkinter.Tk()
    root.title("Bob Ross Canvass")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    main_frame = ttk.Frame(root, padding=5)
    main_frame.grid()

    canvas = tkinter.Canvas(main_frame, background="lightgray", width=400, height=400)
    canvas.grid(columnspan=2)

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=3, column=1)
    quit_button["command"] = lambda: quit_program(mqtt_client)

    my_delegate = MyDelegate(canvas)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    root.bind('<Left>', lambda event: turn_left(mqtt_client))

    root.mainloop()


def quit_program(mqtt_client):
    mqtt_client.close()
    exit()


def turn_left(client):
    client.send_message("turn_left")


main()
