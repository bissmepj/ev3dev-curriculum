
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
def main():
    # DONE: 2. Setup an mqtt_client.  Notice that since you don't need to receive any messages you do NOT need to have
    # a MyDelegate class.  Simply construct the MqttClient with no parameter in the constructor (easy).
    # Delete this line, it was added temporarily so that the code we gave you had no errors.
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3("mosquitto.csse.rose-hulman.edu", 10)

    root = tkinter.Tk()
    root.title("Rescue Drone")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    bomb_code_label = ttk.Label(main_frame, text='Bomb Code')
    bomb_code_label.grid(row=8, column=1)
    bomb_code_entry = ttk.Entry(main_frame, width=16)
    bomb_code_entry.grid(row=9, column=1)

    bomb_entry = ttk.Button(main_frame, text='Enter Code')
    bomb_entry.grid(row=10, column=1)
    bomb_entry['command'] = lambda: defuse_bomb(mqtt_client, int(bomb_code_entry.get()))


    # DONE: 3. Implement the callbacks for the drive buttons. Set both the click and shortcut key callbacks.
    #
    # To help get you started the arm up and down buttons have been implemented.
    # You need to implement the five drive buttons.  One has been writen below to help get you started but is commented
    # out. You will need to change some_callback1 to some better name, then pattern match for other button / key combos.

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: drive_forward(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get()))
    root.bind('<Up>', lambda event: drive_forward(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get())))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    # left_button and '<Left>' key
    left_button['command'] = lambda: turn_left(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get()))
    root.bind('<Left>', lambda event: turn_left(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get())))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: drive_stop(mqtt_client)
    root.bind('<space>', lambda event: drive_stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    # right_button and '<Right>' key
    right_button['command'] = lambda: turn_right(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get()))
    root.bind('<Right>', lambda event: turn_right(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get())))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    # back_button and '<Down>' key
    back_button['command'] = lambda: drive_backward(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get()))
    root.bind('<Down>', lambda event: drive_backward(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get())))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    hostage_rescue = ttk.Button(main_frame, text="Rescue")
    hostage_rescue.grid(row=7, column=0)
    hostage_rescue['command'] = (lambda: rescue_mission(mqtt_client))

    bomb_defusal = ttk.Button(main_frame, text="Defusal")
    bomb_defusal.grid(row=7, column=1)
    bomb_defusal['command'] = (lambda: defusal_mission(mqtt_client))

    recon = ttk.Button(main_frame, text='Recon')
    recon.grid(row=7, column=2)
    recon['command'] = (lambda: recon_mission(mqtt_client))

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------
# DONE: 4. Implement the functions for the drive button callbacks.
def drive_forward(mqtt_client, left, right):
    mqtt_client.send_message("forward", [left, right])


def drive_backward(mqtt_client, left, right):
    mqtt_client.send_message("backward", [left, right])


def drive_stop(mqtt_client):
    mqtt_client.send_message("stop")


def turn_right(mqtt_client, left, right):
    mqtt_client.send_message("right", [left, right])


def turn_left(mqtt_client, left, right):
    mqtt_client.send_message("left", [left, right])
# Arm command callbacks
def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")

def rescue_mission(mqtt_client):
    print('Rescue')
    mqtt_client.send_message("rescue")
def defusal_mission(mqtt_client):
    print('Defusal')
    mqtt_client.send_message('defusal', [])
def recon_mission(mqtt_client):
    print('Recon')
    mqtt_client.send_message('recon')
def defuse_bomb(mqtt_client, code):
    print('Entering Code')
    if code == 7355608:
        print('Bomb Has Been Defused')
        mqtt_client.send_message("defused")

# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
