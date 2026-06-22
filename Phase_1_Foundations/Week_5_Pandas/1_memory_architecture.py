import pandas as pd
import numpy as np
import sys

print("--- Memory Optimization with Pandas ---")

print("Generating a large DataFrame with 1 million rows...")
num_rows = 1_000_000
user_ids = np.arange(1, num_rows + 1)
ratings = np.random.randint(1, 6, size=num_rows)
transactions = np.random.uniform(10.0, 1000.0, size=num_rows)
statuses = np.random.choice(['completed', 'pending', 'failed', 'shipped'], size=num_rows)

df = pd.DataFrame({
    'user_id': user_ids,
    'rating': ratings,
    'transaction_amount': transactions,
    'status': statuses
})

start_memory = df.memory_usage(deep=True).sum() / (1024 ** 2)
print(f"Initial Memory Usage: {start_memory:.2f} MB")
print("Default Data Types:")
print(df.dtypes)

print("\nOptimizing Data Types...")

df['rating'] = pd.to_numeric(df['rating'], downcast='integer')
df['transaction_amount'] = pd.to_numeric(df['transaction_amount'], downcast='float')
df['status'] = df['status'].astype('category')

end_memory = df.memory_usage(deep=True).sum() / (1024 ** 2)
reduction = start_memory - end_memory
print(f"Memory Reduction: {reduction:.2f} MB ({(reduction / start_memory) * 100:.2f}%)")
print(f"Optimized Memory Usage: {end_memory:.2f} MB")
print("Optimized Data Types:")
print(df.dtypes)

print("--- Advanced Indexing ---")

print("Extracting 500000th row using .iloc:")
row_iloc = df.iloc[499999]
print(row_iloc)

print("Extracting all Canceled transactions:")
canceled_transactions = df[df['status'] == 'failed']
print(canceled_transactions)

print("Extracting all transactions with amount > 500:")
high_value_transactions = df[df['transaction_amount'] > 500]
print(high_value_transactions)

print("Extracting all transactions with rating 5 and status 'completed':")
high_rating_completed = df[(df['rating'] == 5) & (df['status'] == 'completed')]
print(f"Found {len(high_rating_completed)} transactions with rating 5 and status 'completed'.")
print(high_rating_completed.head(10))