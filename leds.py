from gpiozero import LED, Button, InputDevice
from Timer import Timer
import time

RED_PIN   = 5
GREEN_PIN = 6
BLUE_PIN  = 13


SWITCH1_PIN = 12
SWITCH2_PIN = 16

###############################################################################
class Switch(InputDevice):
    def __init__(self, pin):
        super().__init__(pin, pull_up=True)

    @property
    def is_closed(self):
        print(f"value for switch on pin {self.pin} is: {self.value}")
        # return 1 if the switch is closed and draining power to gnd
        return int(not self.value)




###############################################################################
class LightsStateMachine():
    STATE_OFF   = "00"
    STATE_BLINK = "01"
    STATE_ROLL  = "10"
    STATE_ON    = "11"
    def __init__(self, red_gpio, green_gpio, blue_gpio, switch1_pin, switch2_pin, interval=1):
        self.red = LED(red_gpio)
        self.green = LED(green_gpio)
        self.blue = LED(blue_gpio)

        self.switch1 = Switch(switch1_pin)
        self.switch2 = Switch(switch2_pin)

        self.interval = interval

        self.timer = Timer()

    def run(self):
        last_state = self.STATE_OFF
        while True:
            current_state = str( self.switch1.is_closed ) + str( self.switch2.is_closed )
            # It's really annoying that Python doesn't have case statements
            # _________________________________________________________________
            if (current_state == self.STATE_OFF):
                self.red.off()
                self.green.off()
                self.blue.off()
            # _________________________________________________________________
            elif (current_state == self.STATE_BLINK):
                # first loop of this state - make sure all LEDs are on to start
                if current_state != last_state:
                    self.red.on()
                    self.green.on()
                    self.blue.on()
                    self.timer.countdown = self.interval
                # else check if our blink timer has ended, toggle the LEDs and reset the timer
                elif not self.timer.countdown:
                    self.red.toggle()
                    self.green.toggle()
                    self.blue.toggle()
                    self.timer.countdown = self.interval
            # _________________________________________________________________
            elif (current_state == self.STATE_ROLL):
                # first loop of this state - make sure all LEDs are in a one-hot configuration
                if current_state != last_state:
                    self.red.on()
                    self.green.off()
                    self.blue.off()
                    self.timer.countdown = self.interval
                elif not self.timer.countdown:
                    values = [self.red.value, self.green.value, self.blue.value]
                    # shift values to the right
                    self.red.value   = values[1]
                    self.green.value = values[2]
                    self.blue.value  = values[0]
                    self.timer.countdown = self.interval
            # _________________________________________________________________
            elif (current_state == self.STATE_ON):
                self.red.on()
                self.green.on()
                self.blue.on()

            last_state = current_state
            print("current state is", current_state)
            time.sleep(0.5)
                

if __name__ == "__main__":
    lsm = LightsStateMachine(RED_PIN, GREEN_PIN, BLUE_PIN, SWITCH1_PIN, SWITCH2_PIN)

    lsm.run()