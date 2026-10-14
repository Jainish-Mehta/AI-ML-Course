import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Safely locate and load the CSV
current_script_path = Path(__file__).resolve()
project_root = current_script_path.parent.parent
csv_path = project_root / "data" / "crypto_prices.csv"

print(f"📊 Loading data from {csv_path.name}...")
df = pd.read_csv(csv_path)

latest_prices = df.drop_duplicates(subset=["Coin"], keep="last")

plt.figure(figsize=(8, 6))

coins = latest_prices["Coin"].str.capitalize()
prices = latest_prices["Price_INR"]

bars = plt.bar(coins, prices, color=['orange', 'purple', 'gold'], edgecolor='black')

plt.yscale('log')

plt.title("Latest Cryptocurrency Prices (INR)", fontsize=16, fontweight='bold')
plt.xlabel("Cryptocurrency", fontsize=12)
plt.ylabel("Price in INR (Logarithmic Scale)", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, f"₹{yval:,.2f}", 
             ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
print("📈 Displaying Bar Chart...")

plt.savefig(project_root / "data" / "crypto_prices_chart.png")
plt.show()