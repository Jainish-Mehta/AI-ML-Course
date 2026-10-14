import sqlite3
import numpy as np
from pathlib import Path
import random

root = Path(__file__).resolve().parent.parent.parent
db_path = root / "db" / "advanced_property_price_prediction" / "advanced_real_estate.db"

# 🛑 THE MASTER ADMINISTRATIVE DICTIONARY (24 Zones)
# Rates are estimated base INR Lakhs per Square Foot
# 🛑 THE MASTER ADMINISTRATIVE DICTIONARY
AHMEDABAD_REGIONS = {
    # Premium / City Core
    'Bodakdev': 0.085, 'Satellite': 0.075, 'Vastrapur': 0.080, 'Thaltej': 0.078,
    'AMC': 0.060, 'Cantonment': 0.080, 'Ahmedabad_City': 0.055, 
    
    # Mid-Range / High-Growth
    'Chandkheda': 0.055, 'Ghatlodia': 0.065, 'Vejalpur': 0.055, 
    'Sabarmati': 0.050, 'Bopal': 0.050, 'Bopal_Ghuma': 0.055, 
    'Gota': 0.045, 'Asarwa': 0.045, 'Maninagar': 0.045, 
    
    # Affordable / Outer Suburbs / Industrial
    'Daskroi': 0.035, 'Naroda': 0.030, 'Sanand_Muni': 0.035, 'Sanand_Taluka': 0.025, 
    'Bavla_Muni': 0.028, 'Bavla_Taluka': 0.020, 'Dholka_Muni': 0.025, 'Dholka_Taluka': 0.018, 
    'Viramgam_Muni': 0.022, 'Viramgam_Taluka': 0.015, 'Bareja': 0.025, 
    'Mandal': 0.012, 'Detroj': 0.012, 'Dhandhuka': 0.012, 'Dholera': 0.022, 'Barwala': 0.015
}

def generate_ahmedabad_data(num_records=10000):
    print(f"⚙️ Generating {num_records:,} records across 24 Ahmedabad Administrative Zones...")
    data = []
    loc_names = list(AHMEDABAD_REGIONS.keys())
    
    for _ in range(num_records):
        loc = random.choice(loc_names)
        base_rate = AHMEDABAD_REGIONS[loc]
        
        sqft = np.random.normal(loc=1500, scale=400) 
        sqft = max(800, min(sqft, 5000)) 
        beds = int(max(1, min(5, round(sqft / 500)))) 
        age = max(0, np.random.normal(loc=10, scale=7)) 
        
        noise = np.random.normal(0, 5.0) 
        price_lakhs = (sqft * base_rate) + (beds * 2.0) - (age * 0.5) + noise
        price_lakhs = max(10.0, price_lakhs) # Absolute minimum 10 Lakhs
        
        data.append((round(sqft, 2), beds, round(age, 1), loc, round(price_lakhs, 2)))
        
    return data

def init_db():
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sqft REAL NOT NULL,
                bedrooms INTEGER NOT NULL,
                age_years REAL NOT NULL,
                location TEXT NOT NULL,
                price_lakhs REAL NOT NULL
            );
        """)
        
        cursor.execute("SELECT COUNT(*) FROM properties;")
        if cursor.fetchone()[0] == 0:
            seed_data = generate_ahmedabad_data(10000)
            cursor.executemany("""
                INSERT INTO properties (sqft, bedrooms, age_years, location, price_lakhs) 
                VALUES (?, ?, ?, ?, ?)
            """, seed_data)
            conn.commit()
            print("✅ 10,000 comprehensive Ahmedabad records injected.")

def fetch_all_data():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sqft, bedrooms, age_years, location, price_lakhs FROM properties;")
        data = cursor.fetchall()
        
    num_features = np.array([[row[0], row[1], row[2]] for row in data])
    locations = [row[3] for row in data]
    prices = np.array([row[4] for row in data])
    return num_features, locations, prices

def log_new_property(sqft, beds, age, location, price):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO properties (sqft, bedrooms, age_years, location, price_lakhs) 
            VALUES (?, ?, ?, ?, ?)
        """, (sqft, beds, age, location, price))
        conn.commit()