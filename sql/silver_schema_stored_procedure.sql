--Creating a stored procedure inside my silver SCHEMA
CREATE OR REPLACE PROCEDURE silver.clean_jumia_laptops()
LANGUAGE plpgsql
AS $$
BEGIN
--Dropping the Silver table if it exists (overwrite logic)
	DROP TABLE IF EXISTS silver.jumia_clean_laptops;

--Creating a fresh cleaned Silver table
	CREATE TABLE silver.jumia_clean_laptops (
	    id SERIAL PRIMARY KEY,
	    brand TEXT,
	    processor TEXT,
	    ram TEXT,
	    storage TEXT,
	    screen_size TEXT,
	    condition TEXT,
	    description TEXT,
	    price TEXT,
	    old_price TEXT,
	    discount TEXT,
	    date DATE
		);

--Inserting cleaned and transformed data from Bronze layer
	INSERT INTO silver.jumia_clean_laptops (
	    brand, processor, ram, storage, screen_size, condition, description,
	    price, old_price, discount, date
		)
	SELECT
	    --Extracting brand (first word in product name)
	    split_part(product_name, ' ', 1) AS brand,
	
	    --Identifying processor type based on product name
	    CASE
	        WHEN product_name ILIKE '%i3%' THEN 'Core i3'
	        WHEN product_name ILIKE '%i5%' THEN 'Core i5'
	        WHEN product_name ILIKE '%i7%' THEN 'Core i7'
	        WHEN product_name ILIKE '%celeron%' THEN 'Celeron'
	        WHEN product_name ILIKE '%pentium%' THEN 'Pentium'
	        WHEN product_name ILIKE '%m1%' THEN 'Apple M1'
	        WHEN product_name ILIKE '%m2%' THEN 'Apple M2'
	        ELSE NULL
	    END AS processor,
	
	    --Extracting RAM
	    (SELECT regexp_match(product_name, '\d{1,2}\s?GB\s?', 'i'))[1] AS ram,
	
	    --Extracting storage (e.g 256GB SSD or 1 TB HDD)
	    CASE
		  WHEN product_name ILIKE '%SSD%' THEN 'SSD'
		  WHEN product_name ILIKE '%HDD%' THEN 'HDD'
		  WHEN product_name ILIKE '%Hard Disk%' THEN 'HDD'
		  ELSE NULL
	    END AS storage
	,
	
	   --Extracting screen size (e.g., 14.0" or 15.6”)
	    REPLACE((SELECT regexp_match(product_name, '\d{1,2}\.\d{1,2}["”]?'))[1], '”', '') AS screen_size,
	
	    --Identifying condition of the laptop
	    CASE
	        WHEN product_name ILIKE '%refurbished%' THEN 'Refurbished'
	        WHEN product_name ILIKE '%new%' THEN 'New'
	        ELSE NULL
	    END AS condition,
	
	    --Extracting description (everything after brand)
	    substring(product_name FROM '\s(.+)') AS description,
	
	    --Copying pricing and metadata
	    new_price,
	    old_price,
	    discount,
	    scraped_on
	FROM bronze.jumia_raw_laptops
	WHERE product_name IS NOT NULL;

--Further cleaning of price-related columns

--Step 1: If a price is a range (e.g., "200 - 450"), keep only the left value
	UPDATE silver.jumia_clean_laptops
	SET price = TRIM(SPLIT_PART(price, '-', 1))
	WHERE price LIKE '%-%';

--Step 2: If an old price is a range (e.g., "200 - 1450"), keep only the right value
	UPDATE silver.jumia_clean_laptops
	SET old_price = TRIM(SPLIT_PART(old_price, '-', 2))
	WHERE old_price LIKE '%-%';

--Step 3: Removing KSh and commas from price
	UPDATE silver.jumia_clean_laptops
	SET price = 
	  CASE 
	    WHEN price = 'N/A' THEN NULL 
	    ELSE REPLACE(REPLACE(price, 'KSh', ''), ',', '')
	  END;

--Step 4: Same cleanup for old_price
	UPDATE silver.jumia_clean_laptops
	SET old_price = 
	  CASE 
	    WHEN old_price = 'N/A' THEN NULL 
	    ELSE REPLACE(REPLACE(old_price, 'KSh', ''), ',', '')
	  END;

--Step 5: Removing % symbol
	UPDATE silver.jumia_clean_laptops
	SET discount = 
	  CASE 
	    WHEN discount = 'N/A' THEN NULL 
	    ELSE REPLACE(discount, '%', '') 
	  END;
--Replacing null values in the column
--condition,storage to refurbished and HDD respectively
	UPDATE silver.jumia_clean_laptops
	SET condition = 'Refurbished'
	WHERE condition IS NULL;

	UPDATE silver.jumia_clean_laptops
	SET storage = 'HDD'
	WHERE storage IS NULL;

--Setting data type for price,old_price and discount column to NUMERIC
	ALTER TABLE silver.jumia_clean_laptops
	ALTER COLUMN price TYPE NUMERIC
	USING price::NUMERIC;


	ALTER TABLE silver.jumia_clean_laptops
	ALTER COLUMN old_price TYPE NUMERIC
	USING old_price::NUMERIC;


	ALTER TABLE silver.jumia_clean_laptops
	ALTER COLUMN discount TYPE NUMERIC
	USING discount::NUMERIC;
END;
$$