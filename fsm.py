import numpy as np
import time
import glob
import serial
from gpiozero import Button, DigitalInputDevice

from gpios import *
from Comm import Comm

TIMEOUT = 2

# def setup_comm():
comm = None
for serial_path in glob.glob("/dev/ttyS*"):
    try:
        comm = Comm(serial_path)
    except serial.SerialException:
        pass

if comm is None:
    raise RuntimeError("Unable to open a serial connection")


# def setup_buttons(comm):
BLUE_BUTTON      = ColorButton( Button("GPIO6", pull_up=False)  ).configure(comm, "Blue",  AUDIO_0, duration=2)
GREEN_BUTTON     = ColorButton( Button("GPIO13", pull_up=False) ).configure(comm, "Green", AUDIO_1, duration=2)
RED_BUTTON       = ColorButton( Button("GPIO19", pull_up=False) ).configure(comm, "Red",   AUDIO_2, duration=2)

TRIANGLE_BUTTON  = ShapeButton( Button("GPIO26", pull_up=False) ).configure(comm, "Triangle", AUDIO_3, duration=2)
SQUARE_BUTTON    = ShapeButton( Button("GPIO12", pull_up=False) ).configure(comm, "Square",   AUDIO_4, duration=2)
CIRCLE_BUTTON    = ShapeButton( Button("GPIO16", pull_up=False) ).configure(comm, "Circle",   AUDIO_5, duration=2)

SWITCH1          = LightSwitch( Button("GPIO10", pull_up=False) ).configure(comm, "top-left",     duration=500)
SWITCH2          = LightSwitch( Button("GPIO11", pull_up=False) ).configure(comm, "top-right",    duration=500)
SWITCH3          = LightSwitch( Button("GPIO8", pull_up=False) ).configure(comm, "bottom-right", duration=500)
SWITCH4          = LightSwitch( Button("GPIO7", pull_up=False) ).configure(comm, "bottom-left",  duration=500)


# GREEN_BUTTON = Button("GPIO21", pull_up = False)
while True:
    # print(f"BLUE_BUTTON     : {BLUE_BUTTON.button.value    }")
    # print(f"GREEN_BUTTON    : {GREEN_BUTTON.button.value   }")
    # print(f"RED_BUTTON      : {RED_BUTTON.button.value     }")
    # print(f"TRIANGLE_BUTTON : {TRIANGLE_BUTTON.button.value}")
    # print(f"SQUARE_BUTTON   : {SQUARE_BUTTON.button.value  }")
    # print(f"CIRCLE_BUTTON   : {CIRCLE_BUTTON.button.value  }")
    # print(f"SWITCH1         : {SWITCH1.button.value        }")
    # print(f"SWITCH2         : {SWITCH2.button.value        }")
    # print(f"SWITCH3         : {SWITCH3.button.value        }")
    # print(f"SWITCH4         : {SWITCH4.button.value        }")
    hdr,data = comm.read()
    if hdr.packet_num >= 0:
        print( "Received: ", str() )

    # print( comm.transmit_text("testtesttesttesttest",dtype="SetColor") )
    time.sleep(0.5)
    # msg = {}

    # # -------------------------------------------------------------------------
    # # if anything has changed recently, then calculate what should be displayed
    # if any(b.rising_edge_pulse for b in ALL_INPUTS):
    #     # white by default
    #     if not all(b.rising_edge_pulse for b in COLOR_BUTTONS):
    #         color = 0xFFFFFF
    #     else:
    #         if BLUE_BUTTON.extended_value:
    #             color |= 0x0000FF
    #         if GREEN_BUTTON.extended_value:
    #             color |= 0x00FF00
    #         if RED_BUTTON.extended_value:
    #             color |= 0xFF0000

    #     msg['color'] = color
    #     # Get most recently pressed shape
    #     shape = most_recently_pressed(TRIANGLE_BUTTON, SQUARE_BUTTON, CIRCLE_BUTTON).name
    #     msg['shape'] = shape
    #     msg['light1'] = True if (SWITCH1.rising_edge_pulse) else False
    #     msg['light2'] = True if (SWITCH2.rising_edge_pulse) else False
    #     msg['light3'] = True if (SWITCH3.rising_edge_pulse) else False
    #     msg['light4'] = True if (SWITCH4.rising_edge_pulse) else False

    # # -------------------------------------------------------------------------
    # # otherwise turn everything off until it's pressed again
    # else:
    #     msg['color'] = 0,
    #     msg['shape'] = ""
    #     msg['light1'] = False
    #     msg['light2'] = False
    #     msg['light3'] = False
    #     msg['light4'] = False


    # try:
    #     comm.transmit_text(json.dumps(msg), "SetFrame")
    #     acknowledged = comm.read()[0]
    # except serial.SerialException:
    #     # attempt to reestablish communication with all serial devices
    #     comm = setup_comm()

    # time.sleep(1)