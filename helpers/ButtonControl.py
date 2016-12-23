import RPi.GPIO as GPIO
import time
from threading import Thread
import config as CONFIG
from helpers.MySqlHelper import SqlHelper


class ButtonControl:
    gpio_list = []

    def __init__(self):
        GPIO.setup(CONFIG.BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_gpio(self):
        sqlConn = SqlHelper()
        sqlStr = """ SELECT gpio FROM gpio_pins """
        for pin in sqlConn.read(sqlStr):
            self.gpio_list.append(pin[0])

    def init_button_listener(self):
        Thread(target=self.button_listener, args=()).start()

    def button_listener(self):
        while True:
            input_state = GPIO.input(CONFIG.BUTTON_GPIO)
            if not input_state:
                self.get_gpio()
                self.execute_button_function()
                time.sleep(0.2)

    def execute_button_function(self):
        for pin in self.gpio_list:
            GPIO.output(pin, CONFIG.GPIO_RELAY_OFFSTATE)
