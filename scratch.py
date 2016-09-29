from datetime import datetime
print(datetime.now())
import json


from psutil import Process
import setproctitle
setproctitle.setproctitle("pirriweb")
print(Process().name())

"""
from helpers.MessageHelper import RMQ
RMQ().publish_message(json.dumps({
    'sid': 54,
    'duration': 3,
    'schedule_id': 0
}))
# negative activates, positive turns off
"""
import calendar
import dateutil

print(calendar.day_name[datetime.today().weekday()].lower())


dtnow = str(datetime.now()).split(' ')[1]
dtnow_miltime = dtnow.split(':')[0] + dtnow.split(':')[1]
print(dtnow_miltime)
#print (dtnow.split(' ')[1].replace(':', ''))

