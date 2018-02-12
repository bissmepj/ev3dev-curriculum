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
        self.x = 200
        self.y = 200
        self.heading = "north"
        self.arm_state = 0  # 0 is down, 1 is up

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

    my_del = MyDelegate(canvas)
    mqtt_client = com.MqttClient(my_del)
    mqtt_client.connect_to_ev3()

    canvas.create_rectangle(my_del.x - 2, my_del.y - 2, my_del.x + 2, my_del.y + 2, fill=my_del.color)

    root.bind('<Left>', lambda event: turn_left(mqtt_client, my_del))
    root.bind('<Right>', lambda event: turn_right(mqtt_client, my_del))
    root.bind('<Up>', lambda event: forward(mqtt_client, my_del, canvas))
    root.bind('<Down>', lambda event: change_arm(mqtt_client, my_del))

    root.mainloop()


def quit_program(mqtt_client):
    mqtt_client.close()
    exit()


def turn_left(client, delegate):
    client.send_message("turn_left")
    time.sleep(1)
    if delegate.heading == "north":
        delegate.heading = "west"
    elif delegate.heading == "west":
        delegate.heading = "south"
    elif delegate.heading == "south":
        delegate.heading = "east"
    elif delegate.heading == "east":
        delegate.heading = "north"


def turn_right(client, delegate):
    client.send_message("turn_right")
    time.sleep(1)
    if delegate.heading == "north":
        delegate.heading = "east"
    elif delegate.heading == "east":
        delegate.heading = "south"
    elif delegate.heading == "south":
        delegate.heading = "west"
    elif delegate.heading == "west":
        delegate.heading = "north"


def forward(client, delegate, canvas):
    client.send_message("forward")
    time.sleep(1)
    if delegate.heading == "north":
        delegate.y -= 4
    elif delegate.heading == "east":
        delegate.x += 4
    elif delegate.heading == "south":
        delegate.y += 4
    elif delegate.heading == "west":
        delegate.x -= 4
    draw(canvas, delegate)


def change_arm(client, my_del):
    client.send_message("arm")
    if my_del.arm_state == 0:
        my_del.arm_state = 1
    else:
        my_del.arm_state = 0


def draw(canvas, my_del):
    if my_del.arm_state == 0:
        canvas.create_rectangle(my_del.x - 2, my_del.y - 2, my_del.x + 2, my_del.y + 2, fill=my_del.color)


main()
