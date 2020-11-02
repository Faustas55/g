--
-- File generated with SQLiteStudio v3.2.1 on Fri Jul 3 09:38:22 2020
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: CSM
DROP TABLE IF EXISTS CSM;

CREATE TABLE CSM (
    Id           INTEGER PRIMARY KEY AUTOINCREMENT,
    SP_firstname TEXT,
    SP_lastname  TEXT,
    country      TEXT
);




COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
