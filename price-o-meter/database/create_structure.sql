CREATE TABLE IF NOT EXISTS products (
	id SERIAL PRIMARY KEY,
	name VARCHAR(200) NOT NULL,
	category VARCHAR(50) NOT NULL,
	date_added TIMESTAMP NOT NULL,
	date_updated TIMESTAMP,
	date_removed TIMESTAMP,
	attributes JSONB,
	CONSTRAINT uniq_name_attr UNIQUE(name, attributes)
);

CREATE TABLE IF NOT EXISTS product_locations (
	id SERIAL PRIMARY KEY,
	product_id INTEGER NOT NULL,
	date_added TIMESTAMP NOT NULL,
	date_removed TIMESTAMP,
	site_name VARCHAR(300),
	site_url VARCHAR(1000),
	CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES products (id)
);

CREATE TABLE IF NOT EXISTS prices (
	id SERIAL PRIMARY KEY,
	product_id INTEGER NOT NULL,
	product_location_id INTEGER NOT NULL,
	price NUMERIC NOT NULL,
	price_currency VARCHAR(30) NOT NULL,
	date_added TIMESTAMP NOT NULL,
	CONSTRAINT uniq_prices UNIQUE(product_id, product_location_id, date_added),
	CONSTRAINT fk_producti_id FOREIGN KEY (product_id) REFERENCES products (id),
	CONSTRAINT fk_producti_location_id FOREIGN KEY (product_location_id) REFERENCES product_locations (id)
);
