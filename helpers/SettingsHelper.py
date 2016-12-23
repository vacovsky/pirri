import pymysql
import config as CONFIG

SETTINGS = {
    'LOCALOFFSET': 0,
    'RMQ_QUEUE': 'pirri',
    'RMQ_HOST': '',
    'RMQ_PORT': 5672,
    'RMQ_USER': '',
    'RMQ_PASS': '',
    'BUTTON_GPIO': 19,
    'COMMON_WIRE_GPIO': 21,
    'GPIO_RELAY_OFFSTATE': 1,
    'GPIO_RELAY_ONSTATE': 0,
    'LOGINUSER': '',
    'LOGINPASS': '',
    'OPENWEATHER_ZIP': 0,
    'OPENWEATHER_UNITS': '',
    'OPENWEATHER_APPID': '',
    'MYSQL_HOST': '192.168.111.50',
    'MYSQL_DB': 'pirri',
    'MYSQL_USER': 'pirri',
    'MYSQL_PASS': 'pirri',
    'ADJUST_FORECAST_WEATHER': False,
    'ADJUST_CURRENT_WEATHER': False,
    'WEATHER_CHECK_INTERVAL': 60,
    'USE_NEWRELIC': None,
    'SQL_DEBUG': False,
    'DEBUG_INFO': True
}


class Settings:
    conn = None
    settings_query = "SELECT * FROM settings"

    def __init__(self):
        self.conn = pymysql.connect(SETTINGS['MYSQL_HOST'],
                                    SETTINGS['MYSQL_USER'],
                                    SETTINGS['MYSQL_PASS'],
                                    SETTINGS['MYSQL_DB'])
        self._map_settings(self._get_settings())

    def _map_settings(self, settings_list):
        global SETTINGS
        # OpenWeatherMap
        SETTINGS['OPENWEATHER_APPID'] = settings_list[1]
        SETTINGS['OPENWEATHER_ZIP'] = settings_list[2]
        SETTINGS['OPENWEATHER_UNITS'] = settings_list[3]
        # RabbitMQ
        SETTINGS['RMQ_HOST'] = settings_list[4]
        SETTINGS['RMQ_USER'] = settings_list[5]
        SETTINGS['RMQ_PASS'] = settings_list[6]
        # Web Admin Login
        SETTINGS['LOGINUSER'] = settings_list[8]
        SETTINGS['LOGINPASS'] = settings_list[7]
        # WEATHER
        SETTINGS['ADJUST_CURRENT_WEATHER'] = settings_list[9] == 1
        SETTINGS['ADJUST_FORECAST_WEATHER'] = settings_list[10] == 1
        # GPIO
        SETTINGS['GPIO_RELAY_ONSTATE'] = settings_list[11]
        SETTINGS['GPIO_RELAY_OFFSTATE'] = settings_list[12]
        # MONITORING
        SETTINGS['USE_NEWRELIC'] = settings_list[13] == 1
        # Locale
        SETTINGS['LOCALOFFSET'] = settings_list[14]

    def _get_settings(self):
        results = []
        c = self.conn.cursor()
        c.execute(self.settings_query)
        for row in c:
            results.append(row)
        if SETTINGS['SQL_DEBUG']:
            print(results)
        return results[0]


Settings()
CONFIG.SETTINGS = SETTINGS
if SETTINGS['DEBUG_INFO']:
    for i in SETTINGS.items():
        print(i)
