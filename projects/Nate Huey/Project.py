
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com

class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in

    def message(self, button_name):
        print("Received: " + button_name)
        message_to_display = "Current action is: {}. ".format(button_name)
        self.display_label.configure(text=message_to_display)


def main():
    root = tkinter.Tk()
    root.title("Figthing Robot")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_side_label = ttk.Label(main_frame, text="Defense")
    left_side_label.grid(row=0, column=0)

    spin = ttk.Button(main_frame, text="Death Spin")
    spin.grid(row=3, column=2)
    spin['command'] = lambda: send_spin(mqtt_client)

    perimeter = ttk.Button(main_frame, text="Perimeter")
    perimeter.grid(row=2, column=0)
    perimeter['command'] = lambda: send_perimeter(mqtt_client)

    follow = ttk.Button(main_frame, text="Follow Enemy")
    follow.grid(row=3, column=0)
    follow['command'] = lambda: send_follow(mqtt_client)

    button_label = ttk.Label(main_frame, text="               ")
    button_label.grid(row=1, column=1)

    button_message = ttk.Label(main_frame, text="--")
    button_message.grid(row=2, column=1)

    right_side_label = ttk.Label(main_frame, text="Offense")
    right_side_label.grid(row=0, column=2)

    seek = ttk.Button(main_frame, text="Seek Enemy")
    seek.grid(row=1, column=2)
    seek['command'] = lambda: send_seek(mqtt_client)

    control = ttk.Button(main_frame, text="Remote Control")
    control.grid(row=2, column=2)
    control['command'] = lambda: send_control(mqtt_client)

    stop = ttk.Button(main_frame, text="Stop")
    stop.grid(row=1, column=0)
    stop['command'] = lambda: send_stop(mqtt_client)

    spacer = ttk.Label(main_frame, text="")
    spacer.grid(row=4, column=2)

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client))

    pc_delegate = MyDelegateOnThePc(button_message)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()
    # mqtt_client.connect_to_ev3("35.194.247.175")  # Off campus IP address of a GCP broker

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------


def send_spin(mqtt_client):
    print('Death Spin')
    mqtt_client.send_message('spin')
def send_stop(mqtt_client):
    print('Stop')
    mqtt_client.send_message('stop')
def send_seek(mqtt_client):
    print('Seek Enemy')
    mqtt_client.send_message('seek')
def send_control(mqtt_client):
    print('User Control')
    mqtt_client.send_message('control')
def send_follow(mqtt_client):
    print('Follow Enemy')
    mqtt_client.send_message('follow')
def send_perimeter(mqtt_client):
    print('Follow Perimeter')
    mqtt_client.send_message('perimeter')



def quit_program(mqtt_client):
    mqtt_client.send_message('quit')
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
