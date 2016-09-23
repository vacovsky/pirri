import RPi.GPIO as GPIO
import time
from threading import Thread


class ButtonControl:
    gpio_pin = 19
    relay_active = False
    relay_pin = 12

    def __init__(self, gpio_pin=19, relay_pin=12):
        self.gpio_pin = gpio_pin
        self.relay_pin = relay_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def init_button_listener(self):
        Thread(target=self.button_listener, args=()).start()

    def button_listener(self):
        while True:
            input_state = GPIO.input(self.gpio_pin)
            if not input_state:
                self.execute_button_function()
                time.sleep(0.3)

    def execute_button_function(self):
        self.relay_active = not self.relay_active
        GPIO.output(self.relay_pin, self.relay_active)
        print("Relay connected to GPIO-{0} status: {1}".format(self.relay_pin, self.relay_active))
