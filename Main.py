import setproctitle
setproctitle.setproctitle("pirri")

import RPi.GPIO as GPIO
from helpers.ScheduleControl import ScheduleControl
from threading import Thread
from helpers.MessageHelper import RMQ
import time
from helpers.ButtonControl import ButtonControl


class Main:

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    def start(self):
        Thread(target=RMQ().listen, args=()).start()
        ButtonControl().init_button_listener()


if __name__ == '__main__':
    try:
        main = Main()
        try:
            ScheduleControl().start_threaded(59)
        except Exception as e:
            print(e)
            time.sleep(15)
            ScheduleControl().start_threaded(59)

        # ButtonControl(relay_pins=main.relay_pins).init_button_listener()
        main.start()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
