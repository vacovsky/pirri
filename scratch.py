from datetime import datetime
print(datetime.now())
import json

from psutil import Process
import setproctitle
setproctitle.setproctitle("pirriweb")
print(Process().name())


from helpers.MessageHelper import RMQ
RMQ().publish_message(json.dumps({
    'sid': 54,
    'duration': 3,
    'schedule_id': 0
}))
# negative activates, positive turns off
