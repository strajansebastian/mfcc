CREATE TABLE IF NOT EXISTS transhadow_products (
	id SERIAL PRIMARY KEY,
	name VARCHAR(200) NOT NULL,
	category VARCHAR(50) NOT NULL,
	date_added TIMESTAMP NOT NULL,
	date_updated TIMESTAMP,
	date_removed TIMESTAMP,
	attributes JSONB,
	CONSTRAINT ts_uniq_name_attr UNIQUE(name, attributes)
);

CREATE TABLE IF NOT EXISTS transhadow_product_locations (
	id SERIAL PRIMARY KEY,
	product_id INTEGER NOT NULL,
	date_added TIMESTAMP NOT NULL,
	date_removed TIMESTAMP,
	site_name VARCHAR(300),
	site_url VARCHAR(1000)
);

CREATE TABLE IF NOT EXISTS transhadow_prices (
	id SERIAL PRIMARY KEY,
	product_id INTEGER NOT NULL,
	product_location_id INTEGER NOT NULL,
	price NUMERIC NOT NULL,
	price_currency VARCHAR(30) NOT NULL,
	date_added TIMESTAMP NOT NULL,
	CONSTRAINT ts_uniq_prices UNIQUE(product_id, product_location_id, date_added)
);

CREATE TABLE IF NOT EXISTS transhadow_locks (
	id SERIAL PRIMARY KEY,
	transaction_id INTEGER NOT NULL,
	transaction_query VARCHAR(4000) NOT NULL,
	locked_table VARCHAR(50) NOT NULL,
        lock_type VARCHAR(25) NOT NULL

);

CREATE TABLE IF NOT EXISTS transhadow_lock_requests (
	transaction_id SERIAL PRIMARY KEY,
	transaction_time TIMESTAMP NOT NULL,
	transaction_status VARCHAR(25) NOT NULL, -- queued, processing, finished
	transaction_state VARCHAR(25) NOT NULL, -- none, commit, rollback
	transaction_query VARCHAR(4000) NOT NULL, -- SELECT, UPDATE, INSERT or DELETE query
	locked_table VARCHAR(50) NOT NULL, -- name of table that is in lock state
        lock_request_type VARCHAR(25) NOT NULL -- read, write
);
