from requests import get
import json

try:
    from data import config as CONFIG
    OPENWEATHER_ZIP = CONFIG.OPENWEATHER_ZIP
    OPENWEATHER_UNITS = CONFIG.OPENWEATHER_UNITS
    OPENWEATHER_APPID = CONFIG.OPENWEATHER_APPID

except:
    OPENWEATHER_ZIP = 93422
    OPENWEATHER_UNITS = "imperial"
    OPENWEATHER_APPID = "0d9330204965c8852145c4a52b56fd1a"


class WeatherHelper:
    units = None
    zip = None
    appid = None
    wh_uris = {
        'current': 'http://api.openweathermap.org/data/2.5/weather?zip={0},us&units={1}&appid={2}',
        'forecast': 'http://api.openweathermap.org/data/2.5/forecast/weekly?lang=english&zip={0},us&units={1}&appid={2}'
    }

    def __init__(self, units=OPENWEATHER_UNITS, zip=OPENWEATHER_ZIP, appid=OPENWEATHER_APPID):
        self.units = units
        self.zip = zip
        self.appid = appid

    def get_current_weather(self):
        data = json.loads(
            get(self.wh_uris['current'].format(self.zip, self.units, self.appid)).text)
        data['wind']['compass_direction'] = self.deg_to_compass(
            data['wind']['deg'])
        return data

    def get_forecast_weather(self):
        data = json.loads(
            get(self.wh_uris['forecast'].format(self.zip, self.units, self.appid)).text)
        return data

    def deg_to_compass(self, num):
        val = int((num / 22.5) + .5)
        arr = ["North", "North-Northeast", "Northeast", "East-Northeast", "East", "East-Southeast", "Southeast", "South-Southeast",
               "South", "South-Southwest", "Southwest", "West-Southwest", "West", "West-Northwest", "Northwest", "North-Northwest"]
        return arr[(val % 16)]

    def rain_extender(self, weather):
        """
        weather = {
            "current": {
                "base": "stations",
                "clouds": {
                    "all": 1
                },
                "cod": 200,
                "coord": {
                    "lat": 35.49,
                    "lon": -120.67
                },
                "dt": 1482213360,
                "id": 5325111,
                "main": {
                    "humidity": 80,
                    "pressure": 1027,
                    "temp": 39.69,
                    "temp_max": 42.8,
                    "temp_min": 37.4
                },
                "name": "Atascadero",
                "sys": {
                    "country": "US",
                    "id": 452,
                    "message": 0.2057,
                    "sunrise": 1482246482,
                    "sunset": 1482281613,
                    "type": 1
                },
                "visibility": 16093,
                "weather": [
                    {
                        "description": "clear sky",
                        "icon": "01n",
                        "id": 800,
                        "main": "Clear"
                    }
                ],
                "wind": {
                    "compass_direction": "Northeast",
                    "deg": 44.0045,
                    "speed": 3.71
                }
            }
        }
        """
        pass

    def heat_extender(self, weather):
        pass

    def freeze_extender(self, weather):
        pass


if __name__ == '__main__':
    # WeatherHelper(units='imperial', zip='93465', appid='0d9330204965c8852145c4a52b56fd1a')
    wh = WeatherHelper()

    print(wh.get_forecast_weather().text)
    print(wh.get_current_weather().text)
