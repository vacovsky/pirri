import pymysql
import dateutil.tz
import datetime
from data import config as CONFIG

SETTINGS = {

    'LOCALOFFSET': -8,
    'QUEUE': 'pirri',
    'DBPATH': '/home/joe/Projects/pirri/data/pirri.sql',
    'RMQ_HOST': 'localhost',
    'RMQ_PORT': 5672,
    'RMQ_USER': '',
    'RMQ_PASS': '',
    'BUTTON_GPIO': 19,
    'COMMON_WIRE_GPIO': 21,
    'GPIO_RELAY_OFFSTATE': 1,
    'GPIO_RELAY_ONSTATE': 0,
    'LOGINUSER': 'joe',
    'LOGINPASS': 'vacovsky',
    'OPENWEATHER_ZIP': 93422,
    'OPENWEATHER_UNITS': "imperial",
    'OPENWEATHER_APPID': "0d9330204965c8852145c4a52b56fd1a",
    'MYSQL_HOST': '192.168.111.50',
    'MYSQL_DB': 'pirri',
    'MYSQL_USER': 'pirri',
    'MYSQL_PASS': 'pirri',
    'USE_SQLITE3': False,
    'USE_MYSQL': True,
    'ADJUST_FORECAST_WEATHER': True,
    'ADJUST_CURRENT_WEATHER': True,
    'WEATHER_CHECK_INTERVAL': 60
}


def populate_settings():
	self.conn = pymysql.connect()
