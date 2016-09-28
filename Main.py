import RPi.GPIO as GPIO
# from ButtonControl import ButtonControl
import setproctitle
from threading import Thread
from helpers.MessageHelper import RMQ


class Main:
    common_pin = 26
    relay_pins = [18, 23, 24, 25, 12, 16, 20, 21, 4, 17, 27, 22, 5, 6, 13]

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

    def start(self):
        Thread(target=RMQ().listen, args=()).start()


if __name__ == '__main__':
    try:
        setproctitle.setproctitle("pirri")
        main = Main()

        # ButtonControl(relay_pins=main.relay_pins).init_button_listener()
        main.start()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
