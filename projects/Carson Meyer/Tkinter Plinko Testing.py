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

import random

import time

import ev3dev.ev3 as ev3

class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in

    def button_pressed(self, button_name):
        print("Received: " + button_name)
        message_to_display = "{} was pressed.".format(button_name)
        self.display_label.configure(text=message_to_display)


def main():
    get_numbers()


def get_numbers():
    seq_x = []
    root = tkinter.Tk()
    root.title("PLINKO!")

    main_frame = ttk.Frame(root, padding=90, relief='raised')
    main_frame.grid()

    sub_title = ttk.Label(main_frame, text="Pick 6 numbers!")
    sub_title.grid(row=1, column=1)

    number_label = ttk.Label(main_frame, text="Numbers")
    number_label.grid(row=3, column=1)

    one_button = ttk.Button(main_frame, text="1")
    one_button.grid(row=4, column=0)
    one_button['command'] = lambda: piece_together(1, seq_x, main_frame, root)

    two_button = ttk.Button(main_frame, text="2")
    two_button.grid(row=4, column=1)
    two_button['command'] = lambda: piece_together(2, seq_x, main_frame, root)

    three_button = ttk.Button(main_frame, text="3")
    three_button.grid(row=4, column=2)
    three_button['command'] = lambda: piece_together(3, seq_x, main_frame, root)

    PLINKO_label = ttk.Label(main_frame, text="  Let's play PLINKO!  ")
    PLINKO_label.grid(row=0, column=1)

    button_message = ttk.Label(main_frame, text="--")
    button_message.grid(row=2, column=1)

    four_button = ttk.Button(main_frame, text="4")
    four_button.grid(row=5, column=0)
    four_button['command'] = lambda: piece_together(4, seq_x, main_frame, root)

    five_button = ttk.Button(main_frame, text="5")
    five_button.grid(row=5, column=1)
    five_button['command'] = lambda: piece_together(5, seq_x, main_frame, root)

    six_button = ttk.Button(main_frame, text="6")
    six_button.grid(row=5, column=2)
    six_button['command'] = lambda: piece_together(6, seq_x, main_frame, root)

    seven_button = ttk.Button(main_frame, text="7")
    seven_button.grid(row=6, column=0)
    seven_button['command'] = lambda: piece_together(7, seq_x, main_frame, root)

    eight_button = ttk.Button(main_frame, text="8")
    eight_button.grid(row=6, column=1)
    eight_button['command'] = lambda: piece_together(8, seq_x, main_frame, root)

    nine_button = ttk.Button(main_frame, text="9")
    nine_button.grid(row=6, column=2)
    nine_button['command'] = lambda: piece_together(9, seq_x, main_frame, root)

    zero_button = ttk.Button(main_frame, text="0")
    zero_button.grid(row=7, column=1)
    zero_button['command'] = lambda: piece_together(0, seq_x, main_frame, root)

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=10, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client))

    pc_delegate = MyDelegateOnThePc(button_message)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()
    # mqtt_client.connect_to_ev3("35.194.247.175")  # Off campus IP address of a GCP broker

    root.mainloop()

    return seq_x


def guess_numbers(root, sequence):
    my_guess = 0
    root.destroy()

    root = tkinter.Tk()
    root.title("PLINKO!")

    main_frame = ttk.Frame(root, padding=25, relief='raised')
    main_frame.grid()

    PLINKO_label = ttk.Label(main_frame, text="  Let's play PLINKO!  ")
    PLINKO_label.grid(row=0, column=1)

    sub_title = ttk.Label(main_frame, text="Which slot will Snatch3r fall out of?")
    sub_title.grid(row=1, column=1)

    one_button = ttk.Button(main_frame, text="1")
    one_button.grid(row=4, column=0)
    one_button['command'] = lambda: which_slot(my_guess, 1, main_frame, sequence, root)

    two_button = ttk.Button(main_frame, text="2")
    two_button.grid(row=4, column=1)
    two_button['command'] = lambda: which_slot(my_guess, 2, main_frame, sequence, root)

    three_button = ttk.Button(main_frame, text="3")
    three_button.grid(row=5, column=0)
    three_button['command'] = lambda: which_slot(my_guess, 3, main_frame, sequence, root)
    four_button = ttk.Button(main_frame, text="4")
    four_button.grid(row=5, column=1)
    four_button['command'] = lambda: which_slot(my_guess, 4, main_frame, sequence, root)

    button_message = ttk.Label(main_frame, text="--")
    button_message.grid(row=2, column=1)

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=10, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client))

    pc_delegate = MyDelegateOnThePc(button_message)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()
    # mqtt_client.connect_to_ev3("35.194.247.175")  # Off campus IP address of a GCP broker

    root.mainloop()


def plinko(sequence, guess, root):
    root.destroy()
    print(sequence)
    print(guess)
    for k in range(6):
        if sequence[k] >= 5:
            print('robot left')

        else:
            print('robot right')

    if my_guess == 2:
        print("You made it!")

    else:
        print("Better luck next time!")


def which_slot(guess, number, main_frame, sequence, root):
    print("My guess is slot {}".format(number))
    guess = number
    next_button = ttk.Button(main_frame, text='Next')
    next_button.grid(row=10, column=0)
    next_button['command'] = lambda: plinko(sequence, guess, root)
    return guess


def shuffle_numbers(seq_x):
    print(seq_x)
    time.sleep(1)
    print("Here comes the shuffle!")
    # ev3.Sound.speak('Here comes the shuffle')
    random.shuffle(seq_x)
    time.sleep(1)
    print(seq_x)


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------
def piece_together(number, sequence, main_frame, root):
    if len(sequence) < 6:
        print('Appending number = {}'.format(number))
        sequence.append(number)
    if 5 < len(sequence) == 6:
        shuffle_numbers(sequence)
        next_button = ttk.Button(main_frame, text='Next')
        next_button.grid(row=10, column=0)
        next_button['command'] = lambda: guess_numbers(root, sequence)


def quit_program(mqtt_client):
    mqtt_client.close()
    exit() #Closes whole process before guessing.  Figure out how to replace, so window closes but doesn't shut down program.


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
seq_x = []
my_guess = 0

main()
