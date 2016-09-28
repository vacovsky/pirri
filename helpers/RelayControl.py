import RPi.GPIO as GPIO
from helpers.SqlHelper import SqlHelper
from datetime import datetime
from data import config as CONFIG
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
            GPIO.setup(pin, GPIO.OUT, initial=1)
            GPIO.output(pin, False)

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
        # self.__reset()
        pin = self.__get_gpio_from_sid(sid)
        self.__log_relay_activity(sid, duration, schedule_id)

        timer = 0
        GPIO.output(pin, not CONFIG.GPIO_RELAY_OFFSTATE)
        GPIO.output(CONFIG.COMMON_WIRE_GPIO, not CONFIG.GPIO_RELAY_OFFSTATE)
        while timer < duration:
            sleep(1)
            timer += 1
        GPIO.output(pin, CONFIG.GPIO_RELAY_OFFSTATE)
        GPIO.output(CONFIG.COMMON_WIRE_GPIO, CONFIG.GPIO_RELAY_OFFSTATE)
