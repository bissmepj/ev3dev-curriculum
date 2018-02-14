#!/usr/bin/env python3
"""
There are no TODOs in this module.  You will simply run this code on your PC to communicate with the EV3.  Feel free
to look at the code to see if you understand what is going on, but no changes are needed to this file.

See the m3_ev3_led_button_communication.py file for all the details.

Author: David Fisher.
"""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in

    def button_pressed(self, button_name):
        print("Received: " + button_name)
        message_to_display = "{} was pressed.".format(button_name)
        self.display_label.configure(text=message_to_display)

def main():
    root = tkinter.Tk()
    root.title("PLINKO!")

    main_frame = ttk.Frame(root, padding=100, relief='raised')
    main_frame.grid()

    sub_title = ttk.Label(main_frame, text="Pick 6 numbers!")
    sub_title.grid(row=1, column=1)

    number_label = ttk.Label(main_frame, text="Numbers")
    number_label.grid(row=3, column=1)

    one_button = ttk.Button(main_frame, text="1")
    one_button.grid(row=4, column=0)
    one_button['command'] = lambda: send_led_command(mqtt_client, "left", "green")

    two_button = ttk.Button(main_frame, text="2")
    two_button.grid(row=4, column=1)
    two_button['command'] = lambda: send_led_command(mqtt_client, "left", "red")

    three_button = ttk.Button(main_frame, text="3")
    three_button.grid(row=4, column=2)
    three_button['command'] = lambda: send_led_command(mqtt_client, "left", "black")

    PLINKO_label = ttk.Label(main_frame, text="  Let's play PLINKO!  ")
    PLINKO_label.grid(row=0, column=1)

    button_message = ttk.Label(main_frame, text="--")
    button_message.grid(row=2, column=1)

    four_button = ttk.Button(main_frame, text="4")
    four_button.grid(row=5, column=0)
    four_button['command'] = lambda: send_led_command(mqtt_client, "right", "green")

    five_button = ttk.Button(main_frame, text="5")
    five_button.grid(row=5, column=1)
    five_button['command'] = lambda: send_led_command(mqtt_client, "right", "red")

    six_button = ttk.Button(main_frame, text="6")
    six_button.grid(row=5, column=2)

    seven_button = ttk.Button(main_frame, text="7")
    seven_button.grid(row=6, column=0)

    eight_button = ttk.Button(main_frame, text="8")
    eight_button.grid(row=6, column=1)

    nine_button = ttk.Button(main_frame, text="9")
    nine_button.grid(row=6, column=2)

    zero_button = ttk.Button(main_frame, text="0")
    zero_button.grid(row=7, column=1)

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=10, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client))

    pc_delegate = MyDelegateOnThePc(button_message)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()
    # mqtt_client.connect_to_ev3("35.194.247.175")  # Off campus IP address of a GCP broker

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------
def send_led_command(mqtt_client, led_side, led_color):
    print("Sending LED side = {}  LED color = {}".format(led_side, led_color))
    mqtt_client.send_message("set_led", [led_side, led_color])


def quit_program(mqtt_client):
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
