import RPi.GPIO as GPIO
import time
from threading import Thread


class ButtonControl:
    phash = {}
    gpio_pin = 19
    relay_active = False
    current_pindex = None
    max_pindex = None
    relay_pins = None
    ptog = {}

    def __init__(self, gpio_pin=19, relay_pins=[]):
        self.gpio_pin = gpio_pin
        self.relay_pins = relay_pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.max_pindex = len(relay_pins) - 1
        self.current_pindex = 0
        self.posctl = 0
        for pin in relay_pins:
            self.ptog[pin] = 1
            GPIO.setup(pin, GPIO.OUT)
            #  GPIO.setup(pin, 1)
            self.phash[pin] = False

    def print_status(self, pin, state):
        print("Relay connected to GPIO-{0} status: {1}".format(pin, state))

    def init_button_listener(self):
        Thread(target=self.button_listener, args=()).start()

    def button_listener(self):
        while True:
            input_state = GPIO.input(self.gpio_pin)
            if not input_state:
                self.execute_button_function()
                time.sleep(0.3)

    def execute_button_function(self):
        self.phash[self.relay_pins[self.current_pindex]] = not self.phash[
            self.relay_pins[self.current_pindex]]
        GPIO.output(
            self.relay_pins[self.current_pindex], self.phash[self.relay_pins[self.current_pindex]])
        self.posctl += 1

        if self.posctl == 2:
            if self.current_pindex < self.max_pindex:
                self.current_pindex += 1
            else:
                self.current_pindex = 0
            self.posctl = 0
