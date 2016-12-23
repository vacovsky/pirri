PORT = 8000
USE_NEWRELIC = True
NEWRELIC_INI_PATH = '/home/joe/Projects/pirri/'
VERSION = 'v1.1.0'

MYSQL_HOST = '192.168.111.50'
MYSQL_DB = 'pirri'
MYSQL_USER = 'pirri'
MYSQL_PASS = 'pirri'


# Most of these entries are overwritten by the settings
# population in helpers/SettingsHelper.py.
# Make changes there.
SETTINGS = {
    'LOCALOFFSET': 0,
    'RMQ_QUEUE': 'pirri',
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
    'OPENWEATHER_ZIP': 0,
    'OPENWEATHER_UNITS': "",
    'OPENWEATHER_APPID': "",
    'MYSQL_HOST': '192.168.111.50',
    'MYSQL_DB': 'pirri',
    'MYSQL_USER': 'pirri',
    'MYSQL_PASS': 'pirri',
    'ADJUST_FORECAST_WEATHER': True,
    'ADJUST_CURRENT_WEATHER': True,
    'WEATHER_CHECK_INTERVAL': 60,
    'USE_NEWRELIC': True,
    'SQL_DEBUG': False
}
