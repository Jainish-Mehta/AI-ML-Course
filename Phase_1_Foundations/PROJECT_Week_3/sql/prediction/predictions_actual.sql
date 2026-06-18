PRAGMA foreign_keys = ON;
CREATE TABLE predictions_actual (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    house_area DECIMAL(10, 2) NOT NULL,
    predicted_price DECIMAL(20, 2) NOT NULL,
    actual_price DECIMAL(20, 2) NOT NULL,
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);