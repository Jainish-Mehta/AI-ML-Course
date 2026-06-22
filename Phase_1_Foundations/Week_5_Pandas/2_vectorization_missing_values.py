import pandas as pd
import numpy as np
import time

print("--- Vectorization ---")

num_rows = 5_000_000

print(f"Generating a DataFrame with {num_rows} rows...")
df_bank = pd.DataFrame({
    'amount': np.random.uniform(10, 1000, size=num_rows)
})

print("Executing slow row-wise operation using .apply()...")
start_time = time.time()
df_bank['tax_slow'] = df_bank['amount'].apply(lambda x: x * 0.05 if x > 250 else x * 0.02)
slow_time = time.time() - start_time 
print(f"Time taken with .apply(): {slow_time:.4f} seconds")

start_time = time.time()
df_bank['tax_fast'] = np.where(df_bank['amount'] > 250, df_bank['amount'] * 0.05, df_bank['amount'] * 0.02)
print("Vectorized operation completed.")
fast_time = time.time() - start_time
print(f"Time taken with vectorized operation: {fast_time:.4f} seconds")

speedup = slow_time / fast_time
print(f"Speedup achieved: {speedup:.2f}x faster with vectorization")

print("\n--- Handling Missing Values ---")

df_missing = pd.DataFrame({
    'user_id': [1, 2, 3, 4, 5],
    'age': [25, 30, np.nan, 35, 40],
    'income': [50000, 60000, 55000, np.nan, 70000]
})

print("Original DataFrame with missing values:")
print(df_missing)

print("Missing values count:")
print(df_missing.isna().sum())

df_dropped = df_missing.dropna()
print("\nDataFrame after dropping rows with missing values:")
print(df_dropped)

print("\nFilling missing values with median:")
df_filled = df_missing.fillna(df_missing.median())
print(df_filled)

