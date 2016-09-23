import RPi.GPIO as GPIO
from ButtonControl import ButtonControl


class Main:
    relay_pin = 12

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12, 0)

    def start(self):
        pass


if __name__ == '__main__':
    main = Main()
    ButtonControl(relay_pin=main.relay_pin).init_button_listener()
    main.start()
