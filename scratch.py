from datetime import datetime


print(datetime.now())


from psutil import Process
import setproctitle

setproctitle.setproctitle("pirriweb")



print(Process().name())

