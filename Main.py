import helpers.SettingsHelper
import config
import setproctitle
setproctitle.setproctitle("pirri")
if config.USE_NEWRELIC:
    try:
        import newrelic.agent
        newrelic.agent.initialize(
            config.NEWRELIC_INI_PATH + 'newrelic_main.ini')
    except:
        print(
            'unable to load new relic.  Is it installed, and do you have a config file?')


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
        try:
            ButtonControl(relay_pins=main.relay_pins).init_button_listener()
        except:
            print("Could not start button controls.")
        main.start()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()
