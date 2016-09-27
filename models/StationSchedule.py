from helpers.SqlHelper import SqlHelper


class StationSchedule:
    sqlConn = SqlHelper()
    sid = None

    def __init__(self, sid):
        self.sid = sid

    def list(self):
        sqlStr = ''' SELECT * FROM schedules where station={0}'''.format(
            self.sid)
        print(self.sqlConn.read(sqlStr))


'''
insert into schedule (id, startdate, enddate, sunday, monday, tuesday, wednesday, thursday, friday, saturday, station, duration, repeat)
 values (3, '20160924', '20450924', 1,1,1,1,1,1,1, 1, 1800, 1)
'''
