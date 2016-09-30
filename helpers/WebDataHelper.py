from helpers.SqlHelper import SqlHelper
from models.Station import Station
from datetime import datetime


def list_gpio():
    sqlConn = SqlHelper()
    gpio_pins = []
    sqlStr = "SELECT * FROM gpio_pins ORDER BY gpio asc"
    pins = sqlConn.read(sqlStr)
    for i in pins:
        gpio_pins.append({
            'gpio': i[0],
            'notes': i[1]
        })
    return gpio_pins


def get_schedule(station=None):
    this_date = int(str(datetime.now().date()).replace('-', ''))
    result = []
    sqlConn = SqlHelper()
    schedules = []
    if station is None:
        sqlStr = """SELECT * FROM schedule WHERE enddate > {0} AND startdate <= {1}""".format(
            this_date, this_date)
        schedules = sqlConn.read(sqlStr)
        for sched in schedules:
            data = {
                "id": sched[0],
                "startdate": sched[1],
                "enddate": sched[2],
                "sunday": sched[3] == 1,
                "monday": sched[4] == 1,
                "tuesday": sched[5] == 1,
                "wednesday": sched[6] == 1,
                "thursday": sched[7] == 1,
                "friday": sched[8] == 1,
                "saturday": sched[9] == 1,
                "station": sched[10],
                "starttime": sched[11],
                "duration": sched[12],
                "repeat": sched[13] == 1
            }
            result.append(data)
        return result


def list_stations():
    sqlConn = SqlHelper()
    stations = []
    sqlStr = 'SELECT * FROM STATIONS ORDER BY ID ASC LIMIT 500'
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


def station_history(sid=None, days=7):
    sqlConn = SqlHelper()
    sqlStr = ""
    if sid is None:
        sqlStr = "SELECT * FROM history WHERE julianday(starttime) >= (julianday('now', '-{0} days')) ORDER BY id DESC".format(
            days)
    else:
        pass
    history_json = {
        'history': []
    }
    for hist in sqlConn.read(sqlStr):
        history_json['history'].append({
            'id': hist[0],
            'sid': hist[1],
            'schedule_id': hist[2],
            'duration': hist[3],
            'starttime': hist[4]
        })
    return history_json


def get_chart_stats(cid, days=30):
    sqlStr = ""
    sqlConn = SqlHelper()
    results = {
        "labels": [],
        "series": [],
        "data": [[]]
    }
    if cid == 1:  # chart1 in js app
        sqlStr = """SELECT DISTINCT sid, SUM(duration / 60)
            FROM history
            WHERE julianday(starttime) >= (julianday('now', '-{0} days'))
            GROUP BY sid
            ORDER BY sid ASC""".format(days)
        td = sqlConn.read(sqlStr)
        for d in td:
            results['labels'].append('SID' + str(d[0]))
            results['data'][0].append(d[1])
        results['series'].append('Usage for the last {0} days'.format(days))

    elif cid == 2:
        pass

    return results


def add_station(sid, gpio_pin):
    Station(sid).add(gpio_pin)


def add_schedule(sid):
    pass


def list_schedules(sid):
    return Station(sid).list_schedules()


def find_last(station_list):
    for station in station_list:
        print()


def find_next(station_list):
    for station in station_list:
        print()
