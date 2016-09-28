from datetime import datetime


print(datetime.now())


from psutil import Process
import setproctitle

setproctitle.setproctitle("pirriweb")


print(Process().name())


from helpers.MessageHelper import RMQ

RMQ().publish_message({
    'sid': 52,
    'duration': 10,
    'schedule_id': 0
})
