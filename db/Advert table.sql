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
  

Alter Table advert
ADD COLUMN comments TEXT;

Alter Table advert
ADD COLUMN SP_firstname TEXT;

Alter Table advert
ADD COLUMN SP_lastname TEXT;

Alter Table advert
ADD COLUMN type TEXT default "Distributor";

Alter Table advert
ADD COLUMN uploaded_date TEXT;

ALTER TABLE advert
ADD COLUMN no_action INTEGER;

ALTER TABLE advert
ADD COLUMN suspected_counterfeiter INTEGER;

ALTER TABLE advert
ADD COLUMN takedown INTEGER;


ALTER TABLE advert
 ADD COLUMN review TEXT; 
 
ALTER TABLE advert
 ADD COLUMN justification TEXT;  
 
ALTER TABLE hades.advert 
  MODIFY COLUMN advert_id INT AUTO_INCREMENT;
