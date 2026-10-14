PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS price_history (
    price_history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    crypto_currency_id INTEGER NOT NULL,
    price DECIMAL(20, 2) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (crypto_currency_id) REFERENCES cryptocurrencies(crypto_currency_id) ON DELETE CASCADE
);
