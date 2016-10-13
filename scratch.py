# # from datetime import datetime
# # print(datetime.now())
# # import json


# # from psutil import Process
# # import setproctitle
# # setproctitle.setproctitle("pirriweb")
# # print(Process().name())


# # from helpers.MessageHelper import RMQ
# # RMQ().publish_message(json.dumps({
# #     'sid': 53,
# #     'duration': 3,
# #     'schedule_id': 0
# # }))
# # # negative activates, positive turns off

# # import calendar
# # import dateutil

# # print(calendar.day_name[datetime.today().weekday()].lower())


# # dtnow = str(datetime.now()).split(' ')[1]
# # dtnow_miltime = dtnow.split(':')[0] + dtnow.split(':')[1]
# # print(dtnow_miltime)
# # #print (dtnow.split(' ')[1].replace(':', ''))



# from dateutil import parser
# from datetime import datetime
# miltime = '700'
# #parser.parse(700)

# converted_time = datetime.time(hour=int(miltime[0:2]), minute=int(miltime[2:4]))

# print
import datetime
base = datetime.datetime.today()
date_list = [base - datetime.timedelta(days=x) for x in range(-6, 7)]  
for i in date_list:
    print (i.date())



print("%04d" % (1,))