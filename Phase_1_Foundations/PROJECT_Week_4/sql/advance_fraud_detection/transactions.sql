PRAGMA foreign_keys = ON;
CREATE TABLE transactions (
    tx_id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_group TEXT NOT NULL,
    purchase_amount REAL NOT NULL
);