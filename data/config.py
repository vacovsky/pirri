QUEUE = 'pirri'
DBPATH = '/home/joe/Projects/pirri/data/pirri.sql'

RMQ_HOST = 'localhost'  # '10.13.17.73'  # "192.168.111.50"  # rmq server address
RMQ_PORT = 5672  # rmq server port
# RMQ_USER = 'rabbit'  # rmq server username
# RMQ_PASS = 'bunnyrabbit!!'  # password to rmq server
RMQ_USER = ''
RMQ_PASS = ''

BUTTON_GPIO = 19
COMMON_WIRE_GPIO = 21
GPIO_RELAY_OFFSTATE = 1
GPIO_RELAY_ONSTATE = 0

#for web app - put this in a database
LOGINUSER = 'joe'
LOGINPASS = 'vacovsky'

OPENWEATHER_ZIP = 93422
OPENWEATHER_UNITS = "imperial"
OPENWEATHER_APPID = "0d9330204965c8852145c4a52b56fd1a"

MYSQL_HOST = '192.168.111.50'
MYSQL_DB = 'pirri'
MYSQL_USER = 'pirri'
MYSQL_PASS = 'pirri'

USE_SQLITE3 = False
USE_MYSQL = True

# GRANT ALL PRIVILEGES ON * TO 'joe'@'%' WITH GRANT OPTION;
# GRANT ALL PRIVILEGES ON mydb.* TO 'myuser'@'%' WITH GRANT OPTION;
