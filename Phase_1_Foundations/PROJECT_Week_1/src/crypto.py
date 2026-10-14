import requests
from datetime import datetime
from pathlib import Path
import csv

class Crypto_Price_Fetcher:
    def __init__(self, coin_name):
        self.coin = coin_name
        self.api_url = "https://api.coingecko.com/api/v3/coins/markets"
        current_dir = Path(__file__).resolve().parent.parent
        self.file_path = current_dir / "data" / "crypto_prices.csv"
        print(f"[{self.coin.upper()}] Tracker Initialized. Fetching price data for {self.coin}...")
        
    def get_price(self):
        payload = {"ids": self.coin,
                   "vs_currencies": "inr"}
        try:
            response = requests.get(self.api_url, params=payload)
            data = response.json()
            price = data[self.coin]['inr']
            return price
        
        except Exception as e:
            print(f"Failed to fetch data: {e}")
            
    def save_data(self, price):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        file_is_new = not self.file_path.exists()
        
        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            
            if file_is_new:
                writer.writerow(["Timestamp", "Coin", "Price_INR"])
                
            writer.writerow([current_time, self.coin, price])
        
        print(f"File saved successfully at {self.file_path} folder")
        
if __name__ == "__main__":
    
    coins=["bitcoin", "ethereum", "dogecoin"]
    
    for coin in coins:
        tracker = Crypto_Price_Fetcher(coin_name=coin)
        live_price = tracker.get_price()
        if live_price is not None:
            print(f"The live price is {live_price} INR")
            tracker.save_data(live_price)