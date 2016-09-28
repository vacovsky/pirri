CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE schedule (
    "id" INTEGER NOT NULL,
    "startdate" INTEGER NOT NULL,
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
CREATE TABLE gpio_pins (
    "gpio" PK INTEGER NOT NULL,
    "notes" TEXT
);
CREATE TABLE "history" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "sid" INTEGER NOT NULL DEFAULT (0),
    "schedule_id" INTEGER,
    "duration" INTEGER NOT NULL DEFAULT (0),
    "starttime" TEXT NOT NULL DEFAULT ('1899-01-01 00:00:00.01')
);
CREATE TABLE "stations" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "gpio" INTEGER NOT NULL DEFAULT (0),
    "notes" TEXT,
    "common" INTEGER
);
