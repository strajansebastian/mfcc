CREATE DATABASE price_o_meter;

CREATE TABLE IF NOT EXISTS price_o_meter.products (
	id INTEGER PRIMARY KEY DEFAULT nextval('serial'),
	name VARCHAR(200) NOT NULL,
	category VARCHAR(50) NOT NULL,
	date_added DATE NOT NULL,
	date_updated DATE,
	date_removed DATE,
	attributes JSONB,
	CONSTRAINT products UNIQUE(name, attributes)
);

CREATE TABLE IF NOT EXISTS price_o_meter.product_locations (
	id INTEGER PRIMARY KEY DEFAULT nextval('serial'),
	product_id INTEGER NOT NULL,
	site_name VARCHAR(300),
	site_url VARCHAR(1000),
	FOREIGN KEY product_id REFERENCES priceo_o_meter.products id
);

CREATE TABLE IF NOT EXISTS price_o_meter.prices (
	id INTEGER PRIMARY KEY DEFAULT nextval('serial'),
	product_id INTEGER NOT NULL,
	product_location_id INTEGER NOT NULL,
	price INTEGER NOT NULL,
	price_currecy VARCHAR(30) NOT NULL,
	date_added DATE NOT NULL,
	CONSTRAINT products UNIQUE(product_id, date_added)
	FOREIGN KEY fk_product_id REFERENCES priceo_o_meter.products id
	FOREIGN KEY fk_product_location_id REFERENCES priceo_o_meter.product_locations id
);
