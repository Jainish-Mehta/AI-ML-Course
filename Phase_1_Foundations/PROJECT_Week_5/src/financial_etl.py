import pandas as pd
import numpy as np
import time
from pathlib import Path

root = Path(__file__).resolve().parent.parent
data_dir = root / "data"
data_dir.mkdir(parents=True, exist_ok=True)
parquet_output = data_dir / "india_transactions.parquet"

print("--- 🏦 INDIAN ENTERPRISE FINANCIAL ETL PIPELINE ---")

def extract_raw_data(num_rows=1_000_000):
    print(f"\n[EXTRACT] Generating {num_rows:,} rows of raw transaction data...")
    
    np.random.seed(42)
    user_ids = np.random.randint(1000, 50000, size=num_rows)
    # Transactions ranging from ₹500 to ₹10,00,000 (10 Lakhs)
    amounts = np.random.uniform(500.0, 1000000.0, size=num_rows)
    # Major Indian Economic States
    locations = np.random.choice(["MH", "KA", "DL", "GJ", "TN"], size=num_rows)
    
    # Inject missing data (Simulating gateway drop-offs)
    nan_indices = np.random.choice(num_rows, size=50000, replace=False)
    amounts[nan_indices] = np.nan
    
    df = pd.DataFrame({
        "user_id": user_ids,
        "amount_inr": amounts,
        "state_code": locations
    })
    return df

def transform_data(df):
    print("\n[TRANSFORM] Executing Data Sanitization & Optimization...")
    start_time = time.time()
    
    # Impute missing transactions with the Median
    median_amount = df['amount_inr'].median()
    df['amount_inr'] = df['amount_inr'].fillna(median_amount)
    
    # Memory Downcasting
    df['user_id'] = pd.to_numeric(df['user_id'], downcast='unsigned') 
    df['amount_inr'] = pd.to_numeric(df['amount_inr'], downcast='float')
    df['state_code'] = df['state_code'].astype('category')
    
    # 🛑 INDIAN RBI COMPLIANCE LOGIC: Flag transactions over ₹5 Lakhs
    df['risk_flag'] = np.where(df['amount_inr'] > 500000.0, 'High Risk (>5L)', 'Standard')
    df['risk_flag'] = df['risk_flag'].astype('category') 
    
    print(f" -> Transformation Complete! Execution Time: {(time.time() - start_time):.2f} sec")
    return df

def load_data(df):
    print("\n[LOAD] Compressing to Apache Parquet...")
    df.to_parquet(parquet_output, engine='pyarrow', compression='snappy')
    print(f"✅ Data safely vaulted at: {parquet_output.name}")

if __name__ == "__main__":
    raw_df = extract_raw_data()
    clean_df = transform_data(raw_df)
    load_data(clean_df)