import pymysql
import dateutil.tz
import datetime
from data import config as CONFIG

SETTINGS = {
    'LOCALOFFSET': -8,
    'QUEUE': 'pirri',
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


class Settings:
    conn = None
    settings_query = "SELECT * FROM SETTINGS"

    def populate_settings(self):
        self.conn = pymysql.connect(SETTINGS['MYSQL_HOST'],
                                    SETTINGS['MYSQL_USER'],
                                    SETTINGS['MYSQL_PASS'],
                                    SETTINGS['MYSQL_DB'])
        self._map_settings(self._get_settings())

    def _map_settings(self, settings_list):
        global SETTINGS
        SETTINGS['OPENWEATHER_APPID'] = settings_list[1]
        SETTINGS['OPENWEATHER_ZIP'] = settings_list[2]
        SETTINGS['OPENWEATHER_UNITS'] = settings_list[3]

        SETTINGS['RMQ_HOST'] = settings_list[3]
        SETTINGS['OPENWEATHER_UNITS'] = settings_list[4]
        SETTINGS['OPENWEATHER_UNITS'] = settings_list[5]
        SETTINGS['OPENWEATHER_UNITS'] = settings_list[6]
        SETTINGS['OPENWEATHER_UNITS'] = settings_list[7]
        SETTINGS['OPENWEATHER_UNITS'] = settings_list[8]
        SETTINGS['OPENWEATHER_UNITS'] = settings_list[9]
        SETTINGS['OPENWEATHER_UNITS'] = settings_list[10]
        SETTINGS['OPENWEATHER_UNITS'] = settings_list[11]
        SETTINGS['OPENWEATHER_UNITS'] = settings_list[12]
        SETTINGS['OPENWEATHER_UNITS'] = settings_list[13]
        SETTINGS['OPENWEATHER_UNITS'] = settings_list[14]
        SETTINGS['OPENWEATHER_UNITS'] = settings_list[15]
        # SETTINGS['OPENWEATHER_UNITS'] = settings_list[3]
        # SETTINGS['OPENWEATHER_UNITS'] = settings_list[3]
        # SETTINGS['OPENWEATHER_UNITS'] = settings_list[3]
        # SETTINGS['OPENWEATHER_UNITS'] = settings_list[3]
        # SETTINGS['OPENWEATHER_UNITS'] = settings_list[3]
        # SETTINGS['OPENWEATHER_UNITS'] = settings_list[3]
        # SETTINGS['OPENWEATHER_UNITS'] = settings_list[3]
        # SETTINGS['OPENWEATHER_UNITS'] = settings_list[3]

    def _get_settings(self):
        c = self.conn.cursor()
        c.execute(self.settings_query)
        return c[0]
