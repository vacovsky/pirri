# import RPi.GPIO as GPIO
from models.StationSchedule import StationSchedule
from helpers.SqlHelper import SqlHelper


class Station:
    sqlConn = None
    sid = None
    gpio_pin = None
    state = 1
    location = ""
    active_ttl = 0
    schedules = []

    def __init__(self, sid):
        self.sid = sid
        self.sqlConn = SqlHelper()

    def load(self):
        try:
            sqlStr = ''' SELECT * FROM STATIONS WHERE id={0}'''.format(
                self.sid)
            data = self.sqlConn.read(sqlStr)[0]
            self.gpio_pin = data[1]
        except Exception as e:
            raise e

    def add(self, gpio_pin):
        try:
            self.gpio_pin = gpio_pin
            sqlStr = '''INSERT INTO stations (ID, GPIO) VALUES ({0}, {1})'''.format(
                self.sid, self.gpio_pin)
            self.sqlConn.execute(sqlStr)
        except Exception as e:
            raise e

    def activate(self, time=900):
        pass

    def deactivate(self):
        pass

    def status(self):
        return self.pin, self.state, self.location, self.active_ttl

    def list_schedules(self):
        return StationSchedule(self.sid).list()
