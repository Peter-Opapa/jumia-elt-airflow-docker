CREATE SCHEMA bronze

CREATE TABLE laptop_data (
    product_name TEXT,
    new_price TEXT,
    old_price TEXT,
    discount TEXT,
    scraped_on TIMESTAMP
);
