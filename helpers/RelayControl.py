import config as CONFIG
from helpers.MySqlHelper import SqlHelper
import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep


class RelayController:

    def __init__(self):
        self.sqlConn = SqlHelper()
        self.__setup_pins()

    def __setup_pins(self):
        pins = []
        sqlStr = """SELECT gpio FROM gpio_pins"""
        for pin in self.sqlConn.read(sqlStr):
            pins.append(pin[0])
        GPIO.setmode(GPIO.BCM)
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT, initial=CONFIG.SETTINGS['GPIO_RELAY_OFFSTATE'])

    def __reset(self):
        GPIO.setmode(GPIO.BCM)
        self.__setup_pins

    def __log_relay_activity(self, sid, duration, schedule_id):
        sqlStr = """ INSERT INTO history (sid, schedule_id, duration, starttime)
        VALUES ({0},{1},{2},'{3}')""".format(
            sid,
            schedule_id,
            duration,
            datetime.now())
        self.sqlConn.execute(sqlStr)

    def __get_gpio_from_sid(self, sid):
        sqlStr = """ SELECT gpio FROM stations WHERE id={0}""".format(sid)
        gpio = self.sqlConn.read(sqlStr)[0]
        return gpio

    def activate_relay(self, sid, duration, schedule_id=0):
        pin = self.__get_gpio_from_sid(sid)
        self.__log_relay_activity(sid, duration, schedule_id)

        timer = 0
        GPIO.output(pin, CONFIG.SETTINGS['GPIO_RELAY_ONSTATE'])
        GPIO.output(CONFIG.SETTINGS['COMMON_WIRE_GPIO'], CONFIG.SETTINGS['GPIO_RELAY_ONSTATE'])
        while timer < duration:
            sleep(1)
            timer += 1
        GPIO.output(pin, CONFIG.SETTINGS['GPIO_RELAY_OFFSTATE'])
        GPIO.output(CONFIG.SETTINGS['COMMON_WIRE_GPIO'], CONFIG.SETTINGS['GPIO_RELAY_OFFSTATE'])
