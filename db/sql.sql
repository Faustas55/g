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
  "polonius_caseid" INTEGER,
  "updated_date" TEXT,
  "uploaded_by" TEXT
);

CREATE INDEX country_category ON advert (
    country,
    category
);


CREATE UNIQUE INDEX unique_SelProdDomain ON advert (
    product,
    seller,
    domain
);
  
