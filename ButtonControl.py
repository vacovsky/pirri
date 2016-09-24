import RPi.GPIO as GPIO
import time
from threading import Thread


class ButtonControl:
    phash = {}
    gpio_pin = 19
    relay_active = False
    relay_pin = 12
    current_pindex = None
    max_pindex = None

    def __init__(self, gpio_pin=19, relay_pins=[]):
        self.gpio_pin = gpio_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.max_pindex = len(relay_pins) - 1
        for pin in relay_pins:
            self.phash[pin] = False

    def init_button_listener(self):
        Thread(target=self.button_listener, args=()).start()

    def button_listener(self):
        while True:
            input_state = GPIO.input(self.gpio_pin)
            if not input_state:
                self.execute_button_function()
                time.sleep(0.3)

    def execute_button_function(self):
        if not self.phash[self.current_pindex]:
            self.phash[self.current_pindex] = not self.phash[
                self.current_pindex]
            GPIO.output(
                self.relay_pins[self.current_pindex], True)
        else:
            GPIO.output(
                self.relay_pins[self.current_pindex], False)
            if self.relay_pins[self.current_pindex] != self.max_pindex:
                self.relay_pins[self.current_pindex] += 1
            else:
                self.relay_pins[self.current_pindex] = 0
        print(
            "Relay connected to GPIO-{0} status: {1}".format(self.relay_pin, self.relay_active))
