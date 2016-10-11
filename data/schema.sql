CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE gpio_pins (
    "gpio" PK INTEGER NOT NULL,
    "notes" TEXT
);
CREATE TABLE "stations" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "gpio" INTEGER NOT NULL DEFAULT (0),
    "notes" TEXT,
    "common" INTEGER
);
CREATE TABLE "history" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "sid" INTEGER NOT NULL DEFAULT (0),
    "schedule_id" INTEGER NOT NULL DEFAULT (0),
    "duration" INTEGER NOT NULL DEFAULT (0),
    "starttime" TEXT
);
CREATE TABLE schedule (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
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
CREATE TABLE dripnodes (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "gph" INTEGER NOT NULL DEFAULT (0),
    "sid" INTEGER NOT NULL DEFAULT (0), 
    "count" INTEGER NOT NULL DEFAULT (0)
);
