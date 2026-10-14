import pandas as pd
from pathlib import Path

# 1. Locate the Parquet file
root = Path(__file__).resolve().parent.parent
parquet_file = root / "data" / "clean_transactions.parquet"

print("⚙️ Decompressing and loading Apache Parquet file into RAM...\n")

# 2. Load the file using Pandas
df = pd.read_parquet(parquet_file, engine='pyarrow')

# 3. Print the results!
print("--- 📊 PARQUET DATA PREVIEW ---")
print(f"Total Rows: {len(df):,}")
print("-" * 50)
print(df.head(10)) # Print just the first 10 rows so we don't crash the terminal!

print("\n--- 🧠 VERIFYING MEMORY TYPES ---")
print("Notice how it remembered our Categorical and Float32 downcasting!")
print(df.dtypes)