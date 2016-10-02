from helpers.SqlHelper import SqlHelper
from models.Station import Station
from datetime import datetime, timedelta
import operator
from dateutil import parser


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


def station_edit(station):
    sqlConn = SqlHelper()
    sqlStr = """UPDATE stations SET
        gpio='{0}',
        notes='{1}'
        WHERE id={2}""".format(
        station['gpio_pin'],
        station['notes'],
        station['sid']
    )
    print(sqlStr)
    sqlConn.execute(sqlStr)


def schedule_edit(schedule, new=False):
    print(schedule)
    sqlConn = SqlHelper()
    sqlStr = """UPDATE schedule SET
        startdate={0},
        enddate={1},
        sunday={2},
        monday={3},
        tuesday={4},
        wednesday={5},
        thursday={6},
        friday={7},
        saturday={8},
        starttime={9},
        duration={10},
        repeat={11},
        station={12}
    WHERE id={13}""".format(
        schedule['startdate'],
        schedule['enddate'],
        schedule['sunday'],
        schedule['monday'],
        schedule['tuesday'],
        schedule['wednesday'],
        schedule['thursday'],
        schedule['friday'],
        schedule['saturday'],
        schedule['starttime'],
        schedule['duration'],
        schedule['repeat'],
        schedule['station'],
        schedule['id']
    )
    print(sqlStr)
    sqlConn.execute(sqlStr)


def schedule_add(schedule):
    print(schedule)
    sqlConn = SqlHelper()
    sqlStr = """INSERT INTO schedule (
            startdate,
            enddate,
            sunday,
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            starttime,
            duration,
            repeat,
            station
        ) VALUES (
            {0},
            {1},
            {2},
            {3},
            {4},
            {5},
            {6},
            {7},
            {8},
            {9},
            {10},
            {11},
            {12})""".format(
        schedule['startdate'],
        schedule['enddate'],
        schedule['sunday'],
        schedule['monday'],
        schedule['tuesday'],
        schedule['wednesday'],
        schedule['thursday'],
        schedule['friday'],
        schedule['saturday'],
        schedule['starttime'],
        schedule['duration'],
        schedule['repeat'],
        schedule['station']
    )
    print(sqlStr)
    sqlConn.execute(sqlStr)


def schedule_delete(schedule_id):
    sqlConn = SqlHelper()
    sqlStr = """DELETE FROM schedule WHERE id={0}""".format(schedule_id)
    sqlConn.execute(sqlStr)


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
    sqlStr = 'SELECT * FROM STATIONS WHERE common=0 ORDER BY ID ASC LIMIT 500'
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
            'details': station.details,
            'schedule': []
        }
        for s in schedules:
            station_json['schedule'].append(s.__dict__)
        stations.append(station_json)
    return stations


def get_last_station_run():
    sqlConn = SqlHelper()
    results = {}
    stations = list_stations()
    for station in stations:
        sqlStr = "SELECT starttime FROM history WHERE sid={0} ORDER BY starttime DESC LIMIT 1".format(
            station['sid'])
        try:
            results[station['sid']] = sqlConn.read(sqlStr)[0][0]
        except:
            results[station['sid']] = '1899-01-01 00:00:00.000000'
    return results


def get_next_station_run():
    today = datetime.now().strftime('%A').lower()
    sqlConn = SqlHelper()
    results = {}
    stations = list_stations()
    for station in stations:
        sqlStr = """SELECT * from schedule
WHERE station=53
AND (starttime > time(strftime('%H%M'), 'now'))

""".format(station['sid'])

        results[station['sid']] = sqlConn.read(sqlStr)[0]
    return results


def chart_stats_chrono(days=7):
    sqlStr = "SELECT sid, starttime, duration FROM history WHERE julianday(starttime) >= (julianday('now', '-{0} days'))".format(
        days)
    sqlConn = SqlHelper()
    results = {
        "labels": [],  # labels = hours?
        "series": [],  # series = station ids
        "data": [[]],  # durations (starttime + sec(duration)), per series
    }
    data = sqlConn.read(sqlStr)
    for d in data:
        # + timedelta(seconds=d[2])))
        results['labels'].append(str(parser.parse(d[1][0:18])))
        results['data'][0].append(d[2] / 60)
    results['series'].append('Active Relay Time (min)')
    return results
    print(results)


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
        "data": []
    }
    station_data = {}
    stations = []
    for s in sqlConn.read("SELECT DISTINCT id FROM stations WHERE common=0"):
        stations.append(s[0])

    for station in stations:
        station_data[station] = {
            station: {
            }
        }

    if cid == 1:  # chart1 in js app

        d1 = []
        sqlStr = """SELECT DISTINCT sid, SUM(duration / 60)
            FROM history
            WHERE julianday(starttime) >= (julianday('now', '-{0} days'))  AND schedule_id>0
            GROUP BY sid
            ORDER BY sid ASC""".format(days)
        td = sqlConn.read(sqlStr)
        for d in td:
            try:
                station_data[d[0]]['scheduled'] = d[1]
            except Exception as e:
                station_data[d[0]]['scheduled'] = 0
        results['series'].append(
            'Scheduled Usage / last {0} days'.format(days))

        d2 = []
        sqlStr = """SELECT DISTINCT sid, SUM(duration / 60)
            FROM history
            WHERE julianday(starttime) >= (julianday('now', '-{0} days')) AND schedule_id=0
            GROUP BY sid
            ORDER BY sid ASC""".format(days)
        td = sqlConn.read(sqlStr)
        for d in td:
            try:
                station_data[d[0]]['unscheduled'] = d[1]
            except Exception as e:
                station_data[d[0]]['unscheduled'] = 0
        results['series'].append(
            'Unscheduled usage / last {0} days'.format(days))

        results['labels'] = stations

        sorted_data = sorted(station_data.items(), key=operator.itemgetter(0))
        for i in sorted_data:
            if 'scheduled' in i[1]:
                d1.append(i[1]['scheduled'])
            else:
                d1.append(0)
            if 'unscheduled' in i[1]:
                d2.append(i[1]['unscheduled'])
            else:
                d2.append(0)
        results['data'].append(d1)
        results['data'].append(d2)

    return results


def add_station(sid, gpio_pin):
    Station(sid).add(gpio_pin)


def list_schedules(sid):
    return Station(sid).list_schedules()


def find_last(station_list):
    for station in station_list:
        print()


def find_next(station_list):
    for station in station_list:
        print()
