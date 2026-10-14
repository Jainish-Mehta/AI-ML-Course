import pandas as pd
import numpy as np
import time
from pathlib import Path

print("--- 📊 1. ADVANCED PANDAS GROUPING ---")

data = {
    'Region': ['North', 'North', 'North', 'South', 'South', 'South', 'East', 'East'],
    'Category': ['Electronics', 'Electronics', 'Apparel', 'Electronics', 'Apparel', 'Apparel', 'Electronics', 'Apparel'],
    'Sales': [1500, 2000, 500, 1200, 800, 900, 3000, 400],
    'Profit': [150, 200, 50, 120, 80, 90, 300, 40]
}
df = pd.DataFrame(data)

grouped_df = df.groupby(['Region', 'Category']).agg({
    'Sales': 'sum',
    'Profit': 'mean' 
})

print("Aggregated Sales and Average Profit by Region & Category:")
print(grouped_df)


print("\n--- 🗄️ 2. THE TRANSITION TO APACHE PARQUET ---")

print("⚙️ Generating 2,000,000 rows of data...")
num_rows = 2_000_000
massive_df = pd.DataFrame({
    'user_id': np.random.randint(1, 10000, size=num_rows),
    'transaction_amount': np.random.uniform(10.0, 1000.0, size=num_rows),
    'status': np.random.choice(["Pending", "Completed", "Failed"], size=num_rows)
})

root = Path(__file__).resolve().parent.parent
data_dir = root / "data"
data_dir.mkdir(parents=True, exist_ok=True)

csv_path = data_dir / "massive_data.csv"
parquet_path = data_dir / "massive_data.parquet"

print("\n⏳ Writing to CSV (This will take a moment)...")
start = time.time()
massive_df.to_csv(csv_path, index=False)
csv_write_time = time.time() - start

print("⚡ Writing to Apache Parquet...")
start = time.time()
# Parquet uses extreme dictionary compression under the hood
massive_df.to_parquet(parquet_path, engine='pyarrow', compression='snappy')
parquet_write_time = time.time() - start

print(f"CSV Write Time    : {csv_write_time:.2f} seconds")
print(f"Parquet Write Time: {parquet_write_time:.2f} seconds")

csv_size = csv_path.stat().st_size / (1024 * 1024) 
parquet_size = parquet_path.stat().st_size / (1024 * 1024)

print("\n📁 Hard Drive Storage Footprint:")
print(f"CSV File Size     : {csv_size:.2f} MB")
print(f"Parquet File Size : {parquet_size:.2f} MB")
print(f"✅ Storage reduced by {((csv_size - parquet_size) / csv_size) * 100:.1f}%!")

# Note: You can delete these massive files from your hard drive after the test!
csv_path.unlink()
parquet_path.unlink()