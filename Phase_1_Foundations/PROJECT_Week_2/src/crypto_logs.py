import sqlite3
import requests
from pathlib import Path

root = Path(__file__).resolve().parent.parent
db_path = root / "db" / "crypto.db"
image_folder = root / "data" / "coin_images"

api_url = "https://api.coingecko.com/api/v3/coins/markets"
payload = {
    "vs_currency": "inr",
    "ids": "bitcoin,ethereum,dogecoin",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": "false",
    "price_change_percentage": "1h,24h,7d"
}

print("📡 Fetching cryptocurrency data...")
try:
    response = requests.get(api_url, params=payload)
    response.raise_for_status()
    market_data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    exit()

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    
    upsert_query = """
    INSERT OR REPLACE INTO crypto_currencies (
        name, symbol, image, market_cap, volume_24h, 
        circulating_supply, total_supply, max_supply, 
        percent_change_1h, percent_change_24h, percent_change_7d
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    history_query = """
    INSERT INTO price_history (crypto_currency_id, price) 
    VALUES (?, ?)
    """
    
    print("Injecting data into Time-Series Database...")
    
    for coin in market_data:
        name = coin.get("name")
        symbol = coin.get("symbol").upper()
        
        image_path = image_folder / f"{name.lower()}.png"
        image_data = None
        if image_path.exists():
            with open(image_path, 'rb') as img_file:
                image_data = img_file.read()

        market_cap = coin.get("market_cap")
        volume_24h = coin.get("total_volume")
        circ_supply = coin.get("circulating_supply")
        total_supply = coin.get("total_supply")
        max_supply = coin.get("max_supply")
        pct_1h = coin.get("price_change_percentage_1h_in_currency")
        pct_24h = coin.get("price_change_percentage_24h_in_currency")
        pct_7d = coin.get("price_change_percentage_7d_in_currency")
        
        data = (
            name, symbol, image_data, market_cap, volume_24h, 
            circ_supply, total_supply, max_supply, 
            pct_1h, pct_24h, pct_7d
        )
        
        cursor.execute(upsert_query, data)
        
        cursor.execute("SELECT crypto_currency_id FROM crypto_currencies WHERE symbol = ?", (symbol,))
        coin_pk = cursor.fetchone()[0]
        
        price = coin.get("current_price")
        cursor.execute(history_query, (coin_pk, price))
        
        print(f"   -> {name}: Updated | History Logged (₹{price:,.2f})")
        
    conn.commit()

print("\nTask completed successfully. Time-Series logged.")