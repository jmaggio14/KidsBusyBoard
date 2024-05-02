from gpiozero import LED, Button, DigitalInputDevice, DigitalOutputDevice
from Timer import Timer
import time
import json

__all__ = [
    # "BLUE_BUTTON",
    # "GREEN_BUTTON",
    # "RED_BUTTON",
    # "TRIANGLE_BUTTON",
    # "SQUARE_BUTTON",
    # "CIRCLE_BUTTON",
    # "SWITCH1",
    # "SWITCH2",
    # "SWITCH3",
    # "SWITCH4",
    # "MISC1",
    # "MISC2",
    # "MISC3",
    # "MISC4",
    'ColorButton',
    'ShapeButton',
    'LightSwitch',
    "MATRIX_PORTAL_A1",
    "MATRIX_PORTAL_A2",
    "MATRIX_PORTAL_A3",
    "MATRIX_PORTAL_A4",
    "AUDIO_0",
    "AUDIO_1",
    "AUDIO_2",
    "AUDIO_3",
    "AUDIO_4",
    "AUDIO_5",
    "AUDIO_6",
    "AUDIO_7",
    "STATUS_LED",
]


# #############################################################################
def pulse_pin(output_device, duration=0.1):
    output_device.on()
    time.sleep(duration)
    output_device.off()


# #############################################################################
class ColorButton():
    def __init__(self, button):
        self.button = button
        self.comm = None
        self.color = None
        self.duration = None
        self.audio_pin = None
        self.button.when_pressed = self.when_pressed
        # kwargs['active_state'] = True
        # kwargs['pull_up'] = False
        # super().__init__(*args, **kwargs)
    # _________________________________________________________________________
    def configure(self, comm, color, audio_pin, duration=2):
        self.comm = comm
        self.color = color
        self.audio_pin = audio_pin
        self.duration = duration
        return self

    # _________________________________________________________________________
    def when_pressed(self):
        msg = {"color":self.color,
                 "duration":self.duration}
        text = json.dumps(msg)
        self.comm.transmit_text(text, dtype="SetColor")
        pulse_pin(self.audio_pin)

        # Pulse 
    

# #############################################################################
class ShapeButton():
    def __init__(self, button):
        self.button = button
        self.comm = None
        self.shape = None
        self.audio_pin = None
        self.duration = None
        # kwargs['active_state'] = True
        # kwargs['pull_up'] = False
        self.button.when_pressed = self.when_pressed
        # super().__init__(*args, **kwargs)
    # _________________________________________________________________________
    def configure(self, comm, shape, audio_pin, duration=2):
        self.comm = comm
        self.shape = shape
        self.audio_pin = audio_pin
        self.duration = duration
        return self

    # _________________________________________________________________________
    def when_pressed(self):
        msg = {"shape":self.shape}
        text = json.dumps(msg)
        self.comm.transmit_text(text, dtype="SetShape")
        pulse_pin(self.audio_pin)


# #############################################################################
class LightSwitch():
    def __init__(self, button):
        self.button = button
        self.comm = None
        self.location = None
        self.duration = None
        # kwargs['active_state'] = True
        # kwargs['pull_up'] = False
        self.button.when_pressed = self.when_pressed
        self.button.when_released = self.when_released
        # super().__init__(*args, **kwargs)   
    # _________________________________________________________________________
    def configure(self, comm, location, duration=10):
        self.comm = comm
        self.location = location
        self.duration = duration
        return self

    # _________________________________________________________________________
    def when_pressed(self):
        msg = {"location":self.location,
                 "duration":self.duration}
        text = json.dumps(msg)
        self.comm.transmit_text(text, dtype="LightOn")

    # _________________________________________________________________________
    def when_released(self):
        msg = {"location":self.location}
        text = json.dumps(msg)
        self.comm.transmit_text(text, dtype="LightOff")


MATRIX_PORTAL_A1 = DigitalOutputDevice("GPIO17", active_high=False, initial_value=1)
MATRIX_PORTAL_A2 = DigitalOutputDevice("GPIO18", active_high=False, initial_value=1)
MATRIX_PORTAL_A3 = DigitalOutputDevice("GPIO27", active_high=False, initial_value=1)
MATRIX_PORTAL_A4 = DigitalOutputDevice("GPIO22", active_high=False, initial_value=1)

AUDIO_0          = MATRIX_PORTAL_A1 
AUDIO_1          = MATRIX_PORTAL_A2 
AUDIO_2          = MATRIX_PORTAL_A3 
AUDIO_3          = MATRIX_PORTAL_A4 
AUDIO_4          = DigitalOutputDevice("GPIO23", active_high=False, initial_value=1) 
AUDIO_5          = DigitalOutputDevice("GPIO24", active_high=False, initial_value=1) 
AUDIO_6          = DigitalOutputDevice("GPIO25", active_high=False, initial_value=1) 
AUDIO_7          = DigitalOutputDevice("GPIO4" , active_high=False, initial_value=1) 

STATUS_LED       = LED("GPIO20")


# BAD = {
#     1  : "3.3v",   #  "3.3v"
#     2  : "5v",     #  "5v"
#     3  : "GPIO8",  #  "GPIO2"
#     4  : "5v",     #  "5v"
#     5  : "GPIO9",  #  "GPIO3"
#     6  : "GND",    #  "GND"
#     7  : "GPIO7",  #  "GPIO4"
#     8  : "TX",     #  "TX"
#     9  : "GND",    #  "GND"
#     10 : "RX",     #  "RX"
    
#     11 : "GPIO0",  #  "GPIO17"
#     12 : "GPIO1",  #  "GPIO18"
#     13 : "GPIO2",  #  "GPIO27"
#     14 : "GND",    #  "GND"
#     15 : "GPIO3",  #  "GPIO22"
#     16 : "GPIO4",  #  "GPIO23"
#     17 : "3.3v",   #  "3.3v"
#     18 : "GPIO5",  #  "GPIO24"
#     19 : "GPIO12", #  "GPIO10"
#     20 : "GND",    #  "GND"
         
#     21 : "GPIO13", #  "GPIO9"
#     22 : "GPIO6",  #  "GPIO25"
#     23 : "GPIO14", #  "GPIO11"
#     24 : "GPIO10", #  "GPIO8"
#     25 : "GND",    #  "GND"
#     26 : "GPIO11", #  "GPIO7"
#     27 : "SDA0",   #  "SDA0"
#     28 : "SCL0",   #  "SCL0"
#     29 : "GPIO21", #  "GPIO5"
#     30 : "GND",    #  "GND"
         
#     31 : "GPIO22", #  "GPIO6"
#     32 : "GPIO26", #  "GPIO12"
#     33 : "GPIO23", #  "GPIO13"
#     34 : "GND",    #  "GND"
#     35 : "GPIO24", #  "GPIO19"
#     36 : "GPIO27", #  "GPIO16"
#     37 : "GPIO25", #  "GPIO26"
#     38 : "GPIO28", #  "GPIO20"
#     39 : "GND",    #  "GND"
#     40 : "GPIO29", #  "GPIO21"
# }

# GOOD = {
#     1  : "3.3v",
#     2  : "5v",
#     3  : "GPIO2",
#     4  : "5v",
#     5  : "GPIO3",
#     6  : "GND",
#     7  : "GPIO4",
#     8  : "TX",
#     9  : "GND",
#     10 : "RX",

#     11 : "GPIO17",
#     12 : "GPIO18",
#     13 : "GPIO27",
#     14 : "GND",
#     15 : "GPIO22",
#     16 : "GPIO23",
#     17 : "3.3v",
#     18 : "GPIO24",
#     19 : "GPIO10",
#     20 : "GND",

#     21 : "GPIO9",
#     22 : "GPIO25",
#     23 : "GPIO11",
#     24 : "GPIO8",
#     25 : "GND",
#     26 : "GPIO7",
#     27 : "SDA0",
#     28 : "SCL0",
#     29 : "GPIO5",
#     30 : "GND",

#     31 : "GPIO6",
#     32 : "GPIO12",
#     33 : "GPIO13",
#     34 : "GND",
#     35 : "GPIO19",
#     36 : "GPIO16",
#     37 : "GPIO26",
#     38 : "GPIO20",
#     39 : "GND",
#     40 : "GPIO21",
# }


# BLUE_BUTTON      = ColorButton("GPIO6").configure (   RisingEdgeButton("BLUE",  ,  pulse_length=2, pull_up=False)
# GREEN_BUTTON     = ColorButton("GPIO13").configure(   RisingEdgeButton("GREEN", , pulse_length=2, pull_up=False)
# RED_BUTTON       = ColorButton("GPIO19").configure(   RisingEdgeButton("RED",   , pulse_length=2, pull_up=False)
# COLOR_BUTTONS = [BLUE_BUTTON, GREEN_BUTTON, RED_BUTTON]


# TRIANGLE_BUTTON  = RisingEdgeButton("TRIANGLE", "GPIO26", pulse_length=2, pull_up=False)
# SQUARE_BUTTON    = RisingEdgeButton("SQUARE",   "GPIO12", pulse_length=2, pull_up=False)
# CIRCLE_BUTTON    = RisingEdgeButton("CIRCLE",   "GPIO16", pulse_length=2, pull_up=False)
# SHAPE_BUTTONS = [TRIANGLE_BUTTON, SQUARE_BUTTON, CIRCLE_BUTTON]


# # SWITCH1          = RisingEdgeButton("SWITCH1", "GPIO2" , pulse_length=0.1, pull_up=False)
# SWITCH2          = RisingEdgeButton("SWITCH2", "GPIO3" , pulse_length=0.1, pull_up=False)
# SWITCH3          = RisingEdgeButton("SWITCH3", "GPIO8",  pulse_length=0.1, pull_up=False)
# SWITCH4          = RisingEdgeButton("SWITCH4", "GPIO7",  pulse_length=0.1, pull_up=False)
# SWITCHES = [SWITCH1, SWITCH2, SWITCH3, SWITCH4]


# MISC1            = RisingEdgeButton("MISC1", "GPIO10", pulse_length=2, pull_up=False)
# MISC2            = RisingEdgeButton("MISC2", "GPIO9",  pulse_length=2, pull_up=False)
# MISC3            = RisingEdgeButton("MISC3", "GPIO11", pulse_length=2, pull_up=False)
# MISC4            = RisingEdgeButton("MISC4", "GPIO5",  pulse_length=2, pull_up=False)
# MISCS = [MISC1, MISC2, MISC3, MISC4]






