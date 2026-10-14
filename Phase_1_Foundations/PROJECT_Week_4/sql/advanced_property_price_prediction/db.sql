CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sqft REAL NOT NULL,
    bedrooms INTEGER NOT NULL,
    age_years REAL NOT NULL,
    state TEXT NOT NULL,
    actual_price REAL NOT NULL
);