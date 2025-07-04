CREATE OR REPLACE PROCEDURE gold.refresh_gold_layer()
LANGUAGE plpgsql
AS $$
BEGIN
	--Droping and recreating GOLD summary tables from the cleaned SILVER layer
	
	-- Droping existing gold table if already exists (ensures fresh data)
	DROP TABLE IF EXISTS gold.brand_price_summary;
	
	-- Brand-level pricing metrics (count, average, min, max price)
	CREATE TABLE gold.brand_price_summary AS
	SELECT
	    brand,
	    COUNT(*) AS total_products,
	    ROUND(AVG(price), 2) AS avg_price,
	    ROUND(MAX(price), 2) AS max_price,
	    ROUND(MIN(price), 2) AS min_price
	FROM silver.jumia_clean_laptops
	WHERE price IS NOT NULL
	GROUP BY brand;
	
	--Droping discount summary if it exists
	DROP TABLE IF EXISTS gold.discount_summary;
	
	-- Discount KPIs per brand (max, min, average)
	CREATE TABLE gold.discount_summary AS
	SELECT
	    brand,
	    MAX(discount) AS max_discount,
	    MIN(discount) AS min_discount,
	    ROUND(AVG(discount), 2) AS avg_discount
	FROM silver.jumia_clean_laptops
	WHERE discount IS NOT NULL
	GROUP BY brand;
	
	--Droping top discounted items table if exists
	DROP TABLE IF EXISTS gold.top_discounted_laptops;
	
	--Top 20 highest discounted laptops for potential deals
	CREATE TABLE gold.top_discounted_laptops AS
	SELECT
	    brand,
	    description,
	    price,
	    old_price,
	    discount
	FROM silver.jumia_clean_laptops
	WHERE discount IS NOT NULL
	ORDER BY discount DESC
	LIMIT 20;
	
	--Droping price trend table if already exists
	DROP TABLE IF EXISTS gold.price_trend;
	
	--Tracking average price change over time
	CREATE TABLE gold.price_trend AS
	SELECT
	    date,
	    ROUND(AVG(price), 2) AS avg_price,
	    ROUND(AVG(old_price), 2) AS avg_old_price
	FROM silver.jumia_clean_laptops
	WHERE price IS NOT NULL
	GROUP BY date
	ORDER BY date;
	
	--Droping condition breakdown table if already exists
	DROP TABLE IF EXISTS gold.condition_summary;
	
	--Counting of laptops by condition (New, Refurbished)
	CREATE TABLE gold.condition_summary AS
	SELECT
	    condition,
	    COUNT(*) AS total
	FROM silver.jumia_clean_laptops
	GROUP BY condition;
	
	--Droping specification summary table if already exists
	DROP TABLE IF EXISTS gold.specs_summary;
	
	--Total count of each RAM and storage configuration
	CREATE TABLE gold.specs_summary AS
	SELECT
	    ram,
	    storage,
	    COUNT(*) AS total
	FROM silver.jumia_clean_laptops
	GROUP BY ram, storage
	ORDER BY total DESC;
END;
$$


