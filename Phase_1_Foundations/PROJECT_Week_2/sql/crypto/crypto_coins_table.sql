PRAGMA foreign_keys = ON;
drop table if exists crypto_currencies;
CREATE TABLE crypto_currencies (
    crypto_currency_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    image BLOB,
    market_cap DECIMAL(20, 2) NOT NULL,
    volume_24h DECIMAL(20, 2) NOT NULL,
    circulating_supply DECIMAL(20, 2) NOT NULL,
    total_supply DECIMAL(20, 2) NOT NULL,
    max_supply DECIMAL(20, 2),
    percent_change_1h DECIMAL(5, 2),
    percent_change_24h DECIMAL(5, 2),
    percent_change_7d DECIMAL(5, 2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
