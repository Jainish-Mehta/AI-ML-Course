import pandas as pd
import numpy as np

# =====================================================================
# 1. TIME-SERIES & FINANCIAL QUANT METHODS (Rolling, Expanding, Shift)
# =====================================================================
print("--- 1. FINANCIAL QUANT METHODS ---")

# Simulating 10 days of stock/crypto closing prices
stock_data = pd.DataFrame({
    'day': pd.date_range(start='2024-01-01', periods=10, freq='D'),
    'close_price': [100.0, 102.0, 101.0, 105.0, 107.0, 106.0, 110.0, 115.0, 112.0, 120.0]
})

# A. Percentage Change (Day-over-Day Returns)
stock_data['daily_return'] = stock_data['close_price'].pct_change()

# B. Rolling Window (3-Day Moving Average)
# Used to smooth out noise in AI time-series forecasting
stock_data['moving_avg_3d'] = stock_data['close_price'].rolling(window=3).mean()

# C. Expanding Window (Cumulative Maximum)
# Tracks the all-time high up to that exact date
stock_data['all_time_high'] = stock_data['close_price'].expanding().max()

print(stock_data[['day', 'close_price', 'daily_return', 'moving_avg_3d', 'all_time_high']].to_string(index=False))


# =====================================================================
# 2. DATA RESHAPING: PIVOT TABLES & MELT
# =====================================================================
print("\n--- 2. RESHAPING: PIVOT TABLE & MELT ---")

# Raw transactional sales across branches and quarters
sales_raw = pd.DataFrame({
    'branch': ['Ahmedabad', 'Ahmedabad', 'Mumbai', 'Mumbai', 'Delhi', 'Delhi'],
    'quarter': ['Q1', 'Q2', 'Q1', 'Q2', 'Q1', 'Q2'],
    'revenue_lakhs': [45, 60, 80, 95, 70, 85]
})

# A. Pivot Table: Transform Long data to Wide Matrix
# Useful for creating correlation matrices and heatmaps
pivot_df = sales_raw.pivot_table(
    index='branch', 
    columns='quarter', 
    values='revenue_lakhs', 
    aggfunc='sum',
    margins=True, # Adds a 'Total' (All) row and column
    margins_name='Total'
)
print("Pivoted Matrix (Wide Format):")
print(pivot_df)

# B. Melt: De-pivot Wide data back to Long Format
# Machine learning algorithms require Long Format (Features as columns, records as rows)
# Resetting index to get 'branch' back as a column
melted_df = pd.melt(
    pivot_df.reset_index(), 
    id_vars=['branch'], 
    value_vars=['Q1', 'Q2'], 
    var_name='quarter', 
    value_name='revenue_lakhs'
)
# Filter out the 'Total' aggregate row
melted_df = melted_df[melted_df['branch'] != 'Total']
print("\nMelted Back to Long Format:")
print(melted_df.to_string(index=False))


# =====================================================================
# 3. SEMI-STRUCTURED DATA: EXPLODE & JSON NORMALIZATION
# =====================================================================
print("\n--- 3. UNPACKING NESTED API PAYLOADS ---")

# Real-world APIs return nested lists and dictionaries inside single columns
nested_users = pd.DataFrame({
    'user_id': [101, 102],
    'skills': [['Python', 'SQL', 'NumPy'], ['Pandas', 'PyTorch']],
    'metadata': [
        {'role': 'Data Engineer', 'experience_yrs': 3},
        {'role': 'ML Architect', 'experience_yrs': 7}
    ]
})

# A. .explode(): Breaks a list into individual rows while keeping other data intact
exploded_df = nested_users.explode('skills').reset_index(drop=True)
print("Exploded List Column (One skill per row):")
print(exploded_df[['user_id', 'skills']])

# B. pd.json_normalize(): Flattens nested JSON/dictionaries into discrete columns
meta_flattened = pd.json_normalize(nested_users['metadata'])
# Merge back with the original user_id
normalized_user_df = pd.concat([nested_users[['user_id']], meta_flattened], axis=1)
print("\nFlattened Dictionary Columns:")
print(normalized_user_df.to_string(index=False))


# =====================================================================
# 4. HIGH-PERFORMANCE EVALUATION: .query() & .eval()
# =====================================================================
print("\n--- 4. NUMEXPR C-ENGINE EXECUTION (.query & .eval) ---")

# In production datasets with 10M rows, standard boolean indexing is slow.
# .query() and .eval() use the NumExpr engine, compiling expressions to C bytecodes.
df_performance = pd.DataFrame({
    'A': np.random.randint(1, 100, size=5),
    'B': np.random.randint(1, 100, size=5),
    'C': np.random.randint(1, 100, size=5)
})

# A. .eval(): Computes algebraic combinations directly in C-memory without allocating intermediate arrays
df_performance['D'] = df_performance.eval('(A * 2) + (B / 2) - C')

# B. .query(): Filters data using clean string expressions
filtered = df_performance.query('A > 50 and D > 0')

print("Evaluated DataFrame:")
print(df_performance)
print("\nFiltered via .query('A > 50 and D > 0'):")
print(filtered)


# =====================================================================
# 5. ENTERPRISE METHOD CHAINING: .pipe()
# =====================================================================
print("\n--- 5. PRODUCTION PIPELINE WITH .pipe() ---")

# Modular, pure functions designed for chaining in ETL pipelines
def clean_outliers(df, column, threshold):
    return df[df[column] <= threshold]

def apply_tax(df, column, rate=0.18):
    df[f'{column}_with_tax'] = df[column] * (1 + rate)
    return df

raw_transactions = pd.DataFrame({
    'tx_id': [1, 2, 3, 4],
    'amount': [500.0, 150000.0, 1200.0, 3500.0] # 150000 is an outlier
})

# .pipe() allows reading data transformations top-to-bottom like an assembly line
pipeline_result = (
    raw_transactions
    .copy()
    .pipe(clean_outliers, column='amount', threshold=10000.0)
    .pipe(apply_tax, column='amount', rate=0.18)
)

print("Pipeline Execution Result (Outlier dropped & 18% Tax applied):")
print(pipeline_result.to_string(index=False))