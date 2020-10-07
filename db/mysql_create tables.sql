Drop table advert;
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
    polonius_caseid         INTEGER DEFAULT NULL,
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

DROP TABLE IF EXISTS CSM;

CREATE TABLE CSM (
    Id           INTEGER PRIMARY KEY AUTO_INCREMENT,
    SP_firstname TEXT,
    SP_lastname  TEXT,
    country      TEXT
);

INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (1, 'Reka', 'Kiss', 'nowhere');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (2, 'Alicia', 'Spivey', 'Canada');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (3, 'Alicia', 'Spivey', 'United States');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (4, 'Rodrigo', 'Silva', 'Brazil');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (5, 'Esteban', 'Arbelaez', 'Mexico');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (6, 'Esteban', 'Arbelaez', 'Peru');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (7, 'Esteban', 'Arbelaez', 'Venezuela');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (8, 'Esteban', 'Arbelaez', 'Guatemala');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (9, 'Esteban', 'Arbelaez', 'Ecuador');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (10, 'Esteban', 'Arbelaez', 'Colombia');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (11, 'Francisco', 'Uceda', 'Argentina');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (12, 'Francisco', 'Uceda', 'Bolivia');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (13, 'Francisco', 'Uceda', 'Chile');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (14, 'Francisco', 'Uceda', 'Uruguay');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (15, 'Francisco', 'Uceda', 'Paraguay');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (16, 'Olena', 'Zaitseva', 'Russia');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (17, 'Olena', 'Zaitseva', 'Ukraine');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (18, 'Nahit_Bartug', 'Yenisehirlioglu', 'Turkey');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (19, 'Nahit_Bartug', 'Yenisehirlioglu', 'United Arab Emirates');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (20, 'Binu', 'Kannookadan', 'Germany');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (21, 'Binu', 'Kannookadan', 'Switzerland');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (22, 'Binu', 'Kannookadan', 'Austria');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (23, 'Atikesh', 'Yelpokonde', 'India');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (24, 'Saadullah', 'Khan', 'Pakistan');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (25, 'FARIA', 'HAQUE', 'Bangladesh');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (26, 'Bao_Ngoc', 'Nguyen', 'Vietnam');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (27, 'Claudine', 'Bao', 'China');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (28, 'Agnes', 'Lee', 'Japan');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (29, 'Agnes', 'Lee', 'Philippines');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (30, 'Agnes', 'Lee', 'South Korea');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (31, 'Agnes', 'Lee', 'Australia');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (32, 'Agnes', 'Lee', 'New Zealand');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (33, 'Agnes', 'Lee', 'Malaysia');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (34, 'Agnes', 'Lee', 'Singapore');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (35, 'Agnes', 'Lee', 'Thailand');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (36, 'Agnes', 'Lee', 'Mayamar');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (37, 'Olena', 'Zaitseva', 'Uzbekistan');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (38, 'Nahit_Bartug', 'Yenisehirlioglu', 'Bulgaria');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (39, 'Agnes', 'Lee', 'Hong Kong');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (40, 'Nahit_Bartug', 'Yenisehirlioglu', 'Iran');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (41, 'Agnes', 'Lee', 'Taiwan');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (42, 'Esteban', 'Arbelaez', 'Panama');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (43, 'Esteban', 'Arbelaez', 'Cuba');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (44, 'Esteban', 'Arbelaez', 'Dominican Republic');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (45, 'Esteban', 'Arbelaez', 'Costa Rica');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (46, 'Esteban', 'Arbelaez', 'Honduras');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (47, 'Esteban', 'Arbelaez', 'El Salvador');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (48, 'Esteban', 'Arbelaez', 'Nicaragua');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (49, 'Esteban', 'Arbelaez', 'Belize');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (50, 'Nahit_Bartug', 'Yenisehirlioglu', 'Israel');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (51, 'Nahit_Bartug', 'Yenisehirlioglu', 'Kuwait');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (52, 'Binu', 'Kannookadan', 'Poland');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (53, 'Binu', 'Kannookadan', 'Czech Republic');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (54, 'Binu', 'Kannookadan', 'Slovakia');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (55, 'Binu', 'Kannookadan', 'Lithuania');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (56, 'Binu', 'Kannookadan', 'Latvia');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (57, 'Binu', 'Kannookadan', 'Estonia');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (58, 'Binu', 'Kannookadan', 'Serbia');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (59, 'Reka', 'Kiss', 'United Kingdom');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (60, 'Reka', 'Kiss', 'Ireland');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (61, 'Reka', 'Kiss', 'Belgium');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (62, 'Reka', 'Kiss', 'Netherlands');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (63, 'Bao_Ngoc', 'Nguyen', 'Cambodia');
INSERT INTO CSM (Id, SP_firstname, SP_lastname, country) VALUES (64, 'Ana_Maria', 'Munteanu', 'Romania');