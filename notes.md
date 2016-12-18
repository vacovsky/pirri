1. pirri process status
1. pirri uptime for app and device
1. pirri app restart button 

2. view schedule for station (search box)
2. ability to view message queue
3. ability to delete all or one item from queue
5. chart for history for single relay/station



insert into history (id, sid, schedule_id, duration, starttime) values (1, 45, 0, 300,'2016-09-29 16:36:10.018883'),
(2, 45, 0, 300,'2016-09-29 16:48:35.197529'),
(3, 47, 0, 300,'2016-09-29 16:53:52.838521'),
(4, 47, 0, 300,'2016-09-29 16:55:40.098622'),
(5, 46, 0, 60, '2016-09-29 16:56:12.464051'),
(6, 48, 0, 60, '2016-09-29 16:57:12.579167'),
(7, 50, 0, 60, '2016-09-29 16:58:12.695324'),
(8, 45, 0, 60, '2016-09-29 18:29:20.907146'),
(9, 48, 0, 60, '2016-09-29 19:48:24.049282'),
(10, 53, 0, 60,'2016-09-29 19:49:24.167811'),
(11, 54, 0, 60,'2016-09-29 19:50:24.283441'),
(12, 45, 0, 60,'2016-09-29 20:41:52.935246'),
(13, 46, 0, 60,'2016-09-29 20:42:39.325506'),
(14, 54, 0, 60,'2016-09-29 21:01:12.130410')


insert into schedule (startdate, enddate, sunday, monday, tuesday, wednesday, thursday, friday, station, starttime, duration, repeat) values (
20160928, 20170923, 1, 1, 1, 1, 1, 1, 1, 1, 1,1)

CREATE TABLE schedule (
	"id" PK AUTOINCREMENT NOT NULL,
	"startdate" INTEGER NOT NULL DEFAULT (18990101),
	"enddate" INTEGER,
	"sunday" INTEGER NOT NULL DEFAULT (0),
	"monday" INTEGER NOT NULL DEFAULT (0),
	"tuesday" INTEGER NOT NULL DEFAULT (0),
	"wednesday" INTEGER NOT NULL DEFAULT (0),
	"thursday" INTEGER NOT NULL DEFAULT (0),
	"friday" INTEGER NOT NULL DEFAULT (0),
	"saturday" INTEGER NOT NULL DEFAULT (0),
	"station" INTEGER NOT NULL DEFAULT (0),
	"starttime" INTEGER NOT NULL DEFAULT (0),
	"duration" INTEGER NOT NULL DEFAULT (0),
	"repeat" INTEGER NOT NULL DEFAULT (0)
);
