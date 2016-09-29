# this needs to be run in a thread, and kick messages off to RMQ for
# execution.

from helpers.MessageHelper import RMQ
import dateutil
import calendar
from datetime import datetime
from helpers.SqlHelper import SqlHelper
from threading import Thread
import time
import json

class ScheduleControl:
    rmq = RMQ()
    last_queued_dur = 0
    sqlConn = SqlHelper()
    last_datetime = ''
    today_cache = None

    def __init__(self):
        self.post_runlist = []
        self.sqlConn = SqlHelper()
        self.rmq = RMQ()

    def start(self):
        while True:
            self.find_now_info()
            self.queue_schedule_items()
            time.sleep(59)

    def queue_schedule_items(self):
        tasks = self.get_current_tasks()
        self.last_datetime = str(self.today_cache['day']) + str(self.today_cache['time'])

        for task in tasks:
            self.rmq.publish_message(
                json.dumps(
                    {
                        'sid': task[1],
                        'schedule_id': task[0],
                        'duration': task[2]
                    }
                )
            )

    def start_threaded(self):
        Thread(target=self.start, args=()).start()

    def find_curr_time(self):
        dtnow = str(datetime.now()).split(' ')[1]
        dtnow_miltime = dtnow.split(':')[0] + dtnow.split(':')[1]
        return int(dtnow_miltime)

    def find_now_info(self):
        self.today_cache = {
            'day': calendar.day_name[datetime.today().weekday()].lower(),
            'time': self.find_curr_time()
        }

    def get_current_tasks(self):
        if str(self.today_cache['day']) + str(self.today_cache['time']) != self.last_datetime:
            sqlStr = """SELECT id, station, duration from schedule
                            where (startdate < date('now') and enddate < date('now'))
                                and {0}=1
                                and starttime={1}
        """.format(
                self.today_cache['day'],
                self.today_cache['time']
            )
            return self.sqlConn.read(sqlStr)
        else:
            pass

    def exec_schedule_item(self, task):
        RMQ().publish_message(task)
