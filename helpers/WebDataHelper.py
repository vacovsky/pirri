from helpers.SqlHelper import SqlHelper
from models.Station import Station
from datetime import datetime, timedelta
import operator
from pytz import timezone, UTC
import random


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


def get_schedule_cal():
    base = datetime.today()
    date_list = [base - timedelta(days=x) for x in range(-6, 7)]
    sqlConn = SqlHelper()
    events = []
    stations = [x[0] for x in sqlConn.read("SELECT id FROM stations")]
    station_colors = {}
    for i in stations:
        station_colors[i] = "#%06x" % random.randint(0, 0xFFFFFF)
    sqlStr = """
        SELECT * FROM schedule
            WHERE (startdate <= replace(date('now'), '-', '')
                AND enddate > replace(date('now'), '-', ''))
        """.format()

    schedules = []
    for sched in sqlConn.read(sqlStr):
        schedules.append(
            {
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
            })
    for date in date_list:
        for event in schedules:
            print(
                str("%04d" % event['starttime'])[:2],
                str("%04d" % event['starttime'])[-2:]
            )
            wd = date.weekday()
            if wd == 0 and event['sunday']:
                events.append({
                    'id': event['id'],
                    'title': "SID #" + str(event['station']) + " for " + str(event['duration'] / 60) + 'minutes',
                    'start': date.replace(date.year, date.month, date.day, int(str("%04d" % event['starttime'])[:2]), int(str("%04d" % event['starttime'])[-2:]), 0),
                    'end': date.replace(date.year, date.month, date.day, int(str("%04d" % event['starttime'])[:2]), int(str("%04d" % event['starttime'])[-2:]), 0) + timedelta(seconds=event['duration']),
                    'backgroundColor': station_colors[event['station']],
                    'textColor': '#FFF'
                })

    return events


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
            results[station['sid']] = None
    return results


def get_next_station_run():
    local = timezone("America/Los_Angeles")
    #  today = datetime.now().strftime('%A').lower()
    today = int(datetime.now().strftime('%w'))
    sqlConn = SqlHelper()
    results = {}
    stations = list_stations()
    sqlStr = """SELECT * FROM schedule
                    WHERE (startdate <= replace(date('now'), '-', '')
                        AND enddate > replace(date('now'), '-', ''))
                        AND station={0}
                    ORDER BY starttime DESC
                            """
    for s in stations:
        results[s['sid']] = {}
        for d in sqlConn.read(sqlStr.format(s['sid'])):
            if s['sid'] == d[10]:
                counter = 0
                counter -= today
                daylist = [d[3], d[4], d[5], d[6], d[7], d[8], d[9]]
                if 1 in daylist:
                    while counter <= 7:
                        counter += 1
                        if daylist[today] == 1 and d[11] > 0:
                            results[s['sid']][
                                'next_date'] = datetime.now().date() + timedelta(days=counter)
                            t = list('{0:04d}'.format(d[11]))
                            t.insert(2, ':')
                            results[s['sid']]['duration'] = d[12]
                            results[s['sid']]['next_time'] = ''.join(t)
                            results[s['sid']]['next_datetime'] = datetime.combine(results[s['sid']]['next_date'], datetime.min.time()) + timedelta(
                                hours=int(
                                    results[s['sid']]['next_time'].split(':')[0]),
                                minutes=int(
                                    results[s['sid']]['next_time'].split(':')[1])
                            )
                            naive = results[s['sid']]['next_datetime']
                            localdt = local.localize(naive, is_dst=True)
                            utc_dt = localdt.astimezone(UTC)
                            if utc_dt < datetime.now().replace(tzinfo=UTC):
                                utc_dt = utc_dt + timedelta(weeks=1)
                            results[s['sid']]['next_datetime'] = utc_dt

                        else:
                            if (today + counter) < 6 and daylist[today + counter] == 1 > 0:
                                results[s['sid']][
                                    'next_date'] = datetime.now().date() + timedelta(days=counter)
                                t = list('{0:04d}'.format(d[11]))
                                t.insert(2, ':')
                                results[s['sid']]['duration'] = d[12]
                                results[s['sid']]['next_time'] = ''.join(t)
                                results[s['sid']]['next_datetime'] = datetime.combine(results[s['sid']]['next_date'], datetime.min.time()) + timedelta(
                                    hours=int(
                                        results[s['sid']]['next_time'].split(':')[0]),
                                    minutes=int(
                                        results[s['sid']]['next_time'].split(':')[1])
                                )
                                naive = results[s['sid']]['next_datetime']
                                localdt = local.localize(naive, is_dst=True)
                                utc_dt = localdt.astimezone(UTC)
                                if utc_dt < datetime.now().replace(tzinfo=UTC):
                                    utc_dt = utc_dt + timedelta(weeks=1)
                                results[s['sid']]['next_datetime'] = utc_dt
    print(results)
    return results


def dripnodes_edit(nodes_data, new=False, delete=False):
    sqlConn = SqlHelper()
    sqlStr = ""
    if new:
        sqlStr = """
            INSERT INTO dripnodes (gph, sid, count) VALUES ({0}, {1}, {2});
        """.format(nodes_data['gph'], nodes_data['sid'], nodes_data['count'])
    elif delete:
        sqlStr = """
            DELETE FROM dripnodes WHERE gph={0} AND sid={1}
        """.format(nodes_data['gph'], nodes_data['sid'])
    else:
        sqlStr = """
            UPDATE dripnodes SET gph={0}, sid={1}, count={2} WHERE sid={1} and gph={0};
        """.format(nodes_data['gph'], nodes_data['sid'], nodes_data['count'])
    sqlConn.execute(sqlStr)


def water_usage_stats():
    sqlConn = SqlHelper()
    sqlStr = """
        SELECT DISTINCT dripnodes.sid,
            SUM((duration / 60 )) as runmins,
            (select sum((gph * [count])) as totalgph from dripnodes where dripnodes.sid=history.sid) as totalgph,
            stations.notes
        FROM history
        INNER JOIN dripnodes ON dripnodes.sid=history.sid
        INNER JOIN stations ON stations.id=history.sid
            WHERE julianday(starttime) >= (julianday('now', '-30 days'))
            GROUP BY dripnodes.sid
            ORDER BY dripnodes.sid ASC;
            """
    results = {'water_usage': []}
    for d in sqlConn.read(sqlStr):
        results['water_usage'].append(
            {
                'sid': d[0],
                'notes': d[3],
                'run_mins': d[1],
                'total_gph': d[2],
                'usage_last_30': (d[1] / 60) * d[2]
            }
        )
    return results


def chart_stats_chrono(days=7):
    sqlConn = SqlHelper()
    sqlStr = """SELECT DISTINCT strftime('%w', starttime) as [day], SUM(duration / 60) as [mins]
            FROM history
            WHERE julianday(starttime) >= (julianday('now', '-7 days'))
            GROUP BY [day]
            ORDER BY [day] ASC""".format(
        days)
    sqlStr2 = """SELECT DISTINCT strftime('%w', starttime) as [day], SUM(duration / 60) as [mins]
            FROM history
            WHERE julianday(starttime) >= (julianday('now', '-7 days')) AND schedule_id>0
            GROUP BY [day]
            ORDER BY [day] ASC""".format(
        days)
    sqlStr3 = """SELECT DISTINCT strftime('%w', starttime) as [day], SUM(duration / 60) as [mins]
            FROM history
            WHERE julianday(starttime) >= (julianday('now', '-7 days')) AND schedule_id=0
            GROUP BY [day]
            ORDER BY [day] ASC""".format(
        days)
    results = {
        "labels": ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        "series": ['Total', 'Scheduled', 'Unscheduled'],
        # durations (starttime + sec(duration)), per series
        "data": [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]]
    }
    # parser.parse('January 11, 2010').strftime("%A")
    sql_data = sqlConn.read(sqlStr)
    sql_data2 = sqlConn.read(sqlStr2)
    sql_data3 = sqlConn.read(sqlStr3)

    for d in sql_data:
        results['data'][0][int(d[0])] = int(d[1])
    for d in sql_data2:
        results['data'][1][int(d[0])] = int(d[1])
    for d in sql_data3:
        results['data'][2][int(d[0])] = int(d[1])

    return results


def chart_stats_chrono_old(days=7):
    sqlStr = "SELECT sid, starttime, duration FROM history WHERE julianday(starttime) >= (julianday('now', '-{0} days'))".format(
        days)
    sqlConn = SqlHelper()
    stationsSql = "SELECT id FROM stations WHERE common=0 ORDER BY id ASC"
    stations = [i[0] for i in sqlConn.read(stationsSql)]
    print(stations)
    results = {
        "labels": [],  # labels = hours?
        "series": [],  # series = station ids
        "data": [[]],  # durations (starttime + sec(duration)), per series
    }
    data = sqlConn.read(sqlStr)
    for day in range(days):
        results['labels'].insert(0, (datetime.now() - timedelta(days=day)))

    for d in data:
        results['data'][0].append(d[2] / 60)
    results['series'] = stations
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
            'Scheduled'.format(days))

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
            'Unscheduled'.format(days))

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


def get_station_nodes():
    sqlConn = SqlHelper()
    sqlStr = """
        SELECT * FROM dripnodes ORDER BY sid ASC
    """
    results = {
        'dripnodes': []
    }
    for dn in sqlConn.read(sqlStr):
        node = {
            'id': dn[0],
            'sid': dn[2],
            'gph': dn[1],
            'count': dn[3]
        }
        results['dripnodes'].append(node)
    return results


def delete_station_node(id):
    sqlConn = SqlHelper()
    sqlStr = """
        DELETE FROM dripnodes WHERE id={0}
    """.format(id)
    sqlConn.execute(sqlStr)


def add_or_edit_station_nodes(dripnode, new=False):
    sqlConn = SqlHelper()
    sqlStr = ""
    if new:
        sqlStr = """
            INSERT INTO dripnodes (gph, sid, count) VALUES ({0},{1},{2})
        """.format(dripnode['gph'], dripnode['sid'], dripnode['count'])
    else:
        sqlStr = """
            UPDATE dripnodes SET gph={0}, sid={1}, count={2} WHERE id={3}
        """.format(dripnode['gph'], dripnode['sid'], dripnode['count'], dripnode['id'])
    sqlConn.execute(sqlStr)


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
