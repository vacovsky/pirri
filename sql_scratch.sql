SELECT * FROM STATIONS
insert into stations (gpio, notes, common) VALUES (21, 'A8', 1),(12, 'A7', 0),(25, 'A6', 0),(16, 'A5', 0),(18, 'A4', 0),(23, 'A3', 0),(6, 'A2', 0),(24, 'A1', 0),(20, 'B8', 0),(26, 'B7', 0),(27, 'B5', 0),(22, 'B4', 0),(5, 'B3', 0),(13, 'B2', 0),(4, 'B1', 0)
CREATE TABLE "main"."stations" ( "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                                                          "gpio" INTEGER NOT NULL DEFAULT (0), "notes" TEXT, "common" INTEGER);