# this needs to be run in a thread, and kick messages off to RMQ for
# execution.

from helpers.MessageHelper import RMQ
import dateutil
import calendar
from datetime import datetime
from helpers.SqlHelper import SqlHelper
from threading import Thread
import time


class ScheduleControl:
    last_queued_dur = 0
    sqlConn = SqlHelper()
    post_runlist = []
    today_cache = None

    def __init__(self):
        self.post_runlist = []
        self.sqlConn = SqlHelper()

    def start(self):
        while True:
            
            time.sleep(self.last_queued_dur)

    def start_threaded(self):
        Thread(target=start, args=()).start()

    def find_curr_time(self):
        dtnow = str(datetime.now()).split(' ')[1]
        dtnow_miltime = dtnow.split(':')[0] + dtnow.split(':')[1]
        return int(dtnow_miltime)

    def find_now_info(self):
        self.today_cache = {
            'day': calendar.day_name[datetime.today().weekday()].lower(),
            'time': self.find_curr_time()
        }

    def get_next_task(self):
        sqlStr = """select * from schedule
where (startdate < date('now') and enddate < date('now'))
    and {0}=1
    and starttime

    """.format(self.today_cache['day'])
        print(self.sqlConn.read(sqlStr))

    def check_schedule(self):
        sqlStr = ''' SELECT * FROM schedules WHERE '''

    def exec_schedule_item(self, task):
        RMQ().publish_message(task)
