# this needs to be run in a thread, and kick messages off to RMQ for
# execution.
from data import config as CONFIG
if CONFIG.USE_MYSQL:
    from helpers.MySqlHelper import SqlHelper
elif CONFIG.USE_MYSQL:
    from helpers.SqlHelper import SqlHelper
else:
    raise Exception(
        "You probably don't have a SQL connector enabled in the data/config.py file.")

import calendar
from datetime import datetime
from helpers.MessageHelper import RMQ
from threading import Thread
import time
import json
import newrelic.agent


class ScheduleControl:
    rmq = RMQ()
    last_queued_dur = 0
    last_datetime = ''
    today_cache = None

    @newrelic.agent.background_task()
    def __init__(self):
        self.post_runlist = []
        self.rmq = RMQ()

    def start(self, check_interval):
        while True:
            self.find_now_info()
            self.queue_schedule_items()
            time.sleep(59)

    @newrelic.agent.background_task()
    def queue_schedule_items(self):
        tasks = self.get_current_tasks()
        self.last_datetime = str(
            self.today_cache['day']) + str(self.today_cache['time'])

        try:
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
        except TypeError as e:
            print(e)

    def start_threaded(self, check_interval):
        Thread(target=self.start, args=(check_interval,)).start()

    @newrelic.agent.background_task()
    def find_curr_time(self):
        dtnow = str(datetime.now()).split(' ')[1]
        dtnow_miltime = dtnow.split(':')[0] + dtnow.split(':')[1]
        return int(dtnow_miltime)

    @newrelic.agent.background_task()
    def find_now_info(self):
        self.today_cache = {
            'day': calendar.day_name[datetime.today().weekday()].lower(),
            'time': self.find_curr_time()
        }

    @newrelic.agent.background_task()
    def get_current_tasks(self):
        sqlConn = SqlHelper()
        if str(self.today_cache['day']) + str(self.today_cache['time']) != self.last_datetime:
            sqlStr = """SELECT id, station, duration from schedule
                        WHERE (
                            startdate <= CAST(replace(date(NOW()), '-', '') AS UNSIGNED)
                                and enddate > CAST(replace(date(NOW()), '-', '') AS UNSIGNED)
                            )
                            and {0}=1
                            and starttime={1}
        """.format(
                self.today_cache['day'],
                self.today_cache['time']
            )
            return sqlConn.read(sqlStr)
        else:
            pass

    @newrelic.agent.background_task()
    def exec_schedule_item(self, task):
        RMQ().publish_message(task)
