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
from datetime import datetime, timedelta
from helpers.MessageHelper import RMQ
from threading import Thread
import time
import json

import newrelic.agent

from helpers.WeatherHelper import WeatherHelper


class ScheduleControl:
    wh = None
    rmq = None
    last_queued_dur = 0
    last_datetime = ''
    today_cache = None

    current_weather = None
    cw_checked = None
    forecast_weather = None
    fw_checked = None

    def __init__(self):
        self.post_runlist = []
        self.rmq = RMQ()
        self.wh = WeatherHelper()

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
            tasks = self.adjust_watering_for_weather(tasks)
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

    def forecast_adjust(self, task):
        # TODO: wire this up
        if self.fw_checked is None or (datetime.now() - self.fw_checked > timedelta(
                minutes=CONFIG.WEATHER_CHECK_INTERVAL * 5)):
            self.forecast = self.wh.get_forecast_weather()
            self.fw_checked = datetime.now()

    def current_adjust(self, task):
        try:
            # if self.cw_checked is None or (datetime.now() - self.cw_checked > timedelta(
            #         minutes=CONFIG.WEATHER_CHECK_INTERVAL)):
            self.current_weather = self.wh.get_current_weather()
            self.cw_checked = datetime.now()
            modified = 1
            modified *= self.wh.rain_skip(self.current_weather)
            modified *= self.wh.heat_extender(self.current_weather)
            modified *= self.wh.freeze_skip(self.current_weather)
            task['duration'] *= modified
            print(str(task))
        except:
            print("Unable to modify watering time based on weather.  Executing run at specified duration.")
        return task

    def adjust_watering_for_weather(self, tasks):
        if CONFIG.ADJUST_CURRENT_WEATHER or CONFIG.ADJUST_FORECAST_WEATHER:
            for task in tasks:
                if CONFIG.ADJUST_CURRENT_WEATHER:
                    self.current_adjust(task)
                if CONFIG.ADJUST_FORECAST_WEATHER:
                    self.forecast_adjust(task)
        return tasks

    def start_threaded(self, check_interval):
        Thread(target=self.start, args=(check_interval,)).start()

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

    def exec_schedule_item(self, task):
        RMQ().publish_message(task)
