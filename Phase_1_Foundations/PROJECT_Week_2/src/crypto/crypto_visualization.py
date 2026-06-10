import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
import io
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

root = Path(__file__).resolve().parent.parent.parent
db_path = root / "db" / "crypto" / "crypto.db"

print("Querying Database for Time-Series History...")
with sqlite3.connect(db_path) as conn:
    query = """
        SELECT 
            c.symbol, 
            c.image,
            p.price, 
            p.recorded_at
        FROM crypto_currencies c
        INNER JOIN price_history p 
            ON c.crypto_currency_id = p.crypto_currency_id
        ORDER BY p.recorded_at ASC;
    """
    
    df = pd.read_sql_query(query, conn)

df['recorded_at'] = pd.to_datetime(df['recorded_at'])

unique_coins = df['symbol'].unique()
num_coins = len(unique_coins)

print(f"Drawing charts for {num_coins} cryptocurrencies...")

fig, axes = plt.subplots(nrows=num_coins, ncols=1, figsize=(10, 4 * num_coins), sharex=False)

if num_coins == 1:
    axes = [axes]

for i, symbol in enumerate(unique_coins):
    ax = axes[i]
    
    coin_data = df[df['symbol'] == symbol]
    
    ax.plot(coin_data['recorded_at'], coin_data['price'], 
            marker='o', linestyle='-', linewidth=2, label=symbol)
    
    ax.set_title(f"Live Price History: {symbol}", fontsize=14, fontweight='bold')
    ax.set_ylabel("Price (INR)", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    img_blob = coin_data['image'].iloc[0] 
    
    if img_blob:
        try:
            img = Image.open(io.BytesIO(img_blob))
            imagebox = OffsetImage(img, zoom=0.05) 
            
            ab = AnnotationBbox(imagebox, (0.02, 1), xycoords='axes fraction', frameon=False)
            ax.add_artist(ab)
        except Exception as e:
            print(f"Could not render image for {symbol}: {e}")
    
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: f"₹{x:,.2f}"))

plt.tight_layout()
print("Displaying Graph...")
plt.savefig(root / "data" / "crypto" / "crypto_price_history_chart.png")
plt.show()