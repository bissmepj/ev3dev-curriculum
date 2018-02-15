"""
The idea behind this project is that the robot acts as a paint brush for a tkinter GUI.
This includes the ability to lift up or put down the paint brush and to select colors.
Quit button on Robot, arrow keys to move, u and j to lift arm
"""

import time
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class MyDelegate(object):

    def __init__(self, canvas, rect, label, label2, label3):
        self.running = True
        self.color = "black"
        self.x = 200
        self.y = 200
        self.heading = "north"
        self.rect = rect
        self.canvas = canvas
        self.heading_label = label
        self.brush_label = label2
        self.color_label = label3
        self.arm_state = 0  # 0 is down, 1 is up

    def color_change(self, lego_color):
        self.color_label["text"] = lego_color
        self.color = lego_color

    def update(self):
        self.canvas.coords(self.rect, [self.x - 2, self.y - 2, self.x + 2, self.y + 2])


def main():
    root = tkinter.Tk()
    root.title("Bob Ross Canvass")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    main_frame = ttk.Frame(root, padding=5)
    main_frame.grid()

    canvas = tkinter.Canvas(main_frame, background="lightgray", width=400, height=400)
    canvas.grid(columnspan=2, rowspan=10)

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=8, column=3)
    quit_button["command"] = lambda: quit_program(mqtt_client)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=3)
    forward_button["command"] = lambda: forward(mqtt_client, my_del, canvas)

    left_button = ttk.Button(main_frame, text="Turn Left")
    left_button.grid(row=3, column=2)
    left_button["command"] = lambda: turn_left(mqtt_client, my_del)

    right_button = ttk.Button(main_frame, text="Turn Right")
    right_button.grid(row=3, column=4)
    right_button["command"] = lambda: turn_right(mqtt_client, my_del)

    brush_button = ttk.Button(main_frame, text="Brush Up/Down")
    brush_button.grid(row=4, column=3)
    brush_button["command"] = lambda: change_arm(mqtt_client, my_del)

    heading_label = ttk.Label(main_frame, text="HEADING -->")
    heading_label.grid(row=5, column=2)
    heading_update_label = ttk.Label(main_frame, text="north")
    heading_update_label.grid(row=5, column=3)

    brush_label = ttk.Label(main_frame, text="Brush State -->")
    brush_label.grid(row=6, column=2)
    brush_update_label = ttk.Label(main_frame, text="Drawing!")
    brush_update_label.grid(row=6, column=3)

    color_label = ttk.Label(main_frame, text="Current Color -->")
    color_label.grid(row=7, column=2)
    color_update_label = ttk.Label(main_frame, text="black")
    color_update_label.grid(row=7, column=3)

    rect = canvas.create_rectangle(198, 198, 202, 202, fill="orange")

    my_del = MyDelegate(canvas, rect, heading_update_label, brush_update_label, color_update_label)
    mqtt_client = com.MqttClient(my_del)
    mqtt_client.connect_to_ev3()

    root.bind('<Left>', lambda event: turn_left(mqtt_client, my_del))
    root.bind('<Right>', lambda event: turn_right(mqtt_client, my_del))
    root.bind('<Up>', lambda event: forward(mqtt_client, my_del, canvas))
    root.bind('<Down>', lambda event: change_arm(mqtt_client, my_del))

    root.mainloop()


def quit_program(mqtt_client):
    mqtt_client.send_message("quit")
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
    delegate.heading_label["text"] = delegate.heading


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
    delegate.heading_label["text"] = delegate.heading


def forward(client, delegate, canvas):
    client.send_message("forward")
    time.sleep(1)
    draw(canvas, delegate)
    if delegate.heading == "north":
        delegate.y -= 4
    elif delegate.heading == "east":
        delegate.x += 4
    elif delegate.heading == "south":
        delegate.y += 4
    elif delegate.heading == "west":
        delegate.x -= 4
    delegate.update()


def change_arm(client, my_del):
    client.send_message("arm")
    time.sleep(3)
    if my_del.arm_state == 0:
        my_del.arm_state = 1
        my_del.brush_label["text"] = "Not Drawing!"
    else:
        my_del.arm_state = 0
        my_del.brush_label["text"] = "Drawing!"


def draw(canvas, my_del):
    if my_del.arm_state == 0:
        canvas.create_rectangle(my_del.x - 2, my_del.y - 2, my_del.x + 2, my_del.y + 2, fill=my_del.color)


main()
