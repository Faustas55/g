START TRANSACTION;

USE hades;

-- Table: advert
DROP TABLE IF EXISTS advert;

CREATE TABLE advert (
    advert_id               INTEGER PRIMARY KEY,
    region                  TEXT,
    country                 TEXT,
    product                 TEXT,
    price                   TEXT,
    cur                     TEXT,
    seller                  TEXT,
    category                TEXT,
    last_seen               TEXT,
    cat                     TEXT,
    domain                  TEXT,
    url                     TEXT,
    date_found              TEXT,
    business                TEXT,
    product_brand           TEXT,
    polonius_caseid         INTEGER,
    updated_date            TEXT,
    updated_by              TEXT,
    type                    VARCHAR(255)  DEFAULT 'Distributor',
    SP_firstname            TEXT,
    SP_lastname             TEXT,
    comments                TEXT,
    uploaded_date           TEXT,
    no_action               INTEGER,
    suspected_counterfeiter INTEGER,
    takedown                INTEGER,
    review                  TEXT,
    justification           TEXT
);

-- Put all the insert into statements here 
-- Insert into blah blah values 

COMMIT ;
