DROP TABLE advert;


CREATE TABLE advert(
  "advert_id" INTEGER PRIMARY KEY,
  "region" TEXT,
  "country" TEXT,
  "product" TEXT,
  "price" TEXT,
  "cur" TEXT,
  "seller" TEXT,
  "category" TEXT,
  "last_seen" TEXT,
  "cat" TEXT,
  "domain" TEXT,
  "url" TEXT,
  "date_found" TEXT,
  "business" TEXT,
  "product_brand" TEXT,
  "Polonius_caseid" INTEGER
);

CREATE INDEX country_idx ON advert (
    country
);

  
