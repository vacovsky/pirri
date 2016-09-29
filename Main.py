import RPi.GPIO as GPIO
from helpers.ScheduleControl import ScheduleControl
# from ButtonControl import ButtonControl
import setproctitle
setproctitle.setproctitle("pirri")

from threading import Thread
from helpers.MessageHelper import RMQ


class Main:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

    def start(self):
        Thread(target=RMQ().listen, args=()).start()


if __name__ == '__main__':
    try:
        main = Main()
        ScheduleControl().start_threaded(59)
        # ButtonControl(relay_pins=main.relay_pins).init_button_listener()
        main.start()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
