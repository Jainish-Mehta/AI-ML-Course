import sqlite3
import numpy as np
from pathlib import Path

db_path = Path(__file__).resolve().parent.parent.parent / "db" / "prediction" / "price_predictor.db"

def init_db():
    """Initializes the MLOps telemetry table and SEEDS starter data."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions_actual (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                house_area DECIMAL(10, 2) NOT NULL,
                predicted_price DECIMAL(20, 2) NOT NULL,
                actual_price DECIMAL(20, 2) NOT NULL,
                prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 🛑 FIX 1: Save the 5 starter houses directly into the database!
        cursor.execute("SELECT COUNT(*) FROM predictions_actual;")
        if cursor.fetchone()[0] == 0:
            seed_data = [
                (1.0, 150.0, 150.0), 
                (1.5, 220.0, 220.0), 
                (2.0, 280.0, 280.0), 
                (2.5, 360.0, 360.0), 
                (3.0, 410.0, 410.0)
            ]
            cursor.executemany("INSERT INTO predictions_actual (house_area, predicted_price, actual_price) VALUES (?, ?, ?);", seed_data)
            conn.commit()

def get_training_data():
    """Extracts data from the DB."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT house_area, actual_price FROM predictions_actual;")
        data = cursor.fetchall()
        
    # No fallback needed here anymore, because the DB will always have at least 5 rows!
    X_features = np.array([row[0] for row in data])
    y_prices = np.array([row[1] for row in data])
        
    return X_features, y_prices     

def train_polynomial_model(X_features, y_prices):
    """Executes the Normal Equation to find Polynomial Weights."""
    X_reshaped = X_features.reshape(-1, 1)
    X_squared = (X_features ** 2).reshape(-1, 1) 
    bias_column = np.ones((len(X_features), 1))
    
    X_matrix = np.hstack((bias_column, X_reshaped, X_squared))
    
    X_T = X_matrix.T
    weights = np.linalg.inv(X_T @ X_matrix) @ X_T @ y_prices
    
    return weights[0], weights[1], weights[2] 

def log_telemetry(sqft, predicted_price, actual_price):
    """Saves the prediction vs actual result into the database."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO predictions_actual (house_area, predicted_price, actual_price) 
            VALUES (?, ?, ?);
        """, (sqft, predicted_price, actual_price))
        conn.commit()