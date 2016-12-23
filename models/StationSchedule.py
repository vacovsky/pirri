from helpers.MySqlHelper import SqlHelper


class StationSchedule:
    sched_id = None
    sid = None
    startdate = None
    enddate = None

    sunday = 0
    monday = 0
    tuesday = 0
    wednesday = 0
    thursday = 0
    friday = 0
    saturday = 0

    starttime = None
    duration = 0
    repeat = 0

    def __init__(self, sid):
        self.sid = sid

    def list(self):
        schedules = []
        sqlStr = ''' SELECT * FROM schedule where station={0}'''.format(
            self.sid)

        sqlConn = SqlHelper()
        sched_data = sqlConn.read(sqlStr)
        for sched in sched_data:
            s = StationSchedule(self.sid)
            s.sched_id = sched[0]
            s.startdate = sched[1]
            s.enddate = sched[2]

            s.sunday = sched[3]
            s.monday = sched[4]
            s.tuesday = sched[5]
            s.wednesday = sched[6]
            s.thursday = sched[7]
            s.friday = sched[8]
            s.saturday = sched[9]

            s.sid = self.sid  # sched[10]
            s.starttime = sched[11]
            s.duration = sched[12]
            s.repeat = sched[13]

            schedules.append(s)

        return schedules


'''
insert into schedule (id, startdate, enddate, sunday, monday, tuesday, wednesday, thursday, friday, saturday, station, duration, repeat)
 values (3, '20160924', '20450924', 1,1,1,1,1,1,1, 1, 1800, 1)
'''
