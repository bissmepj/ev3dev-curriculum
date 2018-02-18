
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com

class MyDelegateOnPc(object):

    def rescued(self):
        print("Hostage was Rescued")






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
