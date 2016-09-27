from helpers.SqlHelper import SqlHelper
from models.Station import Station


def list_stations():
    sqlConn = SqlHelper()
    stations = []
    sqlStr = 'SELECT * FROM STATIONS LIMIT 500'
    data = sqlConn.read(sqlStr)
    for s in data:
        sid = s[0]
        station = Station(sid)
        station.load()
        schedules = station.list_schedules()
        station_json = {
            'gpio_pin': station.gpio_pin,
            'sid': station.sid,
            'notes': station.notes,
            'schedule': []
        }
        for s in schedules:
            station_json['schedule'].append(s.__dict__)
        stations.append(station_json)
    return stations


def add_station(sid, gpio_pin):
    Station(sid).add(gpio_pin)


def list_schedules(sid):
    return Station(sid).list_schedules()
