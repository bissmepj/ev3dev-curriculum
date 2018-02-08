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

class MyDelegate(object):

    def __init__(self, tkinter_frame):
        self.running = True


def main():
    root = tkinter.Tk()
    root.title("LED Button communication")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()