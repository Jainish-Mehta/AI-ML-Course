import pandas as pd
import numpy as np

# =====================================================================
# 1. pd.concat(): ROW STACKING (AXIS 0) vs COLUMN BINDING (AXIS 1)
# =====================================================================
print("--- 1. CONCATENATION MECHANICS ---")

# Simulating monthly sales data coming from two different branches
branch_ahmedabad = pd.DataFrame({
    'transaction_id': [101, 102],
    'amount': [5000, 7500]
})

branch_mumbai = pd.DataFrame({
    'transaction_id': [201, 202],
    'amount': [12000, 8500]
})

# A. Row-wise Concatenation (Axis 0)
# Stacking rows vertically. ignore_index=True resets the index (0, 1, 2, 3)
all_branches = pd.concat([branch_ahmedabad, branch_mumbai], axis=0, ignore_index=True)
print("Row-wise Stacked (Axis 0):")
print(all_branches)

# B. Column-wise Concatenation (Axis 1)
# Attaching new feature columns side-by-side (must have matching row counts)
user_scores = pd.DataFrame({'credit_score': [750, 680, 810, 720]})
combined_matrix = pd.concat([all_branches, user_scores], axis=1)
print("\nColumn-wise Bound (Axis 1):")
print(combined_matrix)


# =====================================================================
# 2. pd.merge() WITH PRODUCTION SAFEGUARDS (indicator & validate)
# =====================================================================
print("\n--- 2. PRODUCTION MERGING SAFEGUARDS ---")

users = pd.DataFrame({
    'user_id': [1, 2, 3],
    'name': ['Aarav', 'Diya', 'Karan']
})

kyc_records = pd.DataFrame({
    'user_id': [1, 2],
    'kyc_status': ['Verified', 'Pending']
})

# indicator=True adds a '_merge' column showing if the record was in 'left_only', 'right_only', or 'both'
# validate='1:1' mathematically enforces that user_id is unique on BOTH sides (prevents accidental row duplication)
merged_audit = pd.merge(users, kyc_records, on='user_id', how='left', indicator=True, validate='1:1')
print("Merge Audit (Notice the _merge column tracking data origin):")
print(merged_audit)


# =====================================================================
# 3. .transform(): GROUP CALCULATIONS WITHOUT COLLAPSING
# =====================================================================
print("\n--- 3. GROUP TRANSFORMATION (Preserving Row Count) ---")

products = pd.DataFrame({
    'category': ['Electronics', 'Electronics', 'Electronics', 'Clothing', 'Clothing'],
    'item': ['Laptop', 'Mouse', 'Keyboard', 'Shirt', 'Jeans'],
    'price': [60000, 1200, 3500, 1500, 2500]
})

# Normal .groupby().mean() collapses the table to 2 rows.
# .transform() calculates the group mean, but broadcasts it back across all 5 original rows!
products['category_avg_price'] = products.groupby('category')['price'].transform('mean')

# Now you can instantly calculate how much an item deviates from its category baseline
products['diff_from_avg'] = products['price'] - products['category_avg_price']
print("Group Transform Output (Essential for Feature Engineering):")
print(products)


# =====================================================================
# 4. VECTORIZED BOUNDARY FILTRATION: .isin() & .between()
# =====================================================================
print("\n--- 4. CLEAN FILTERING (.isin & .between) ---")

orders = pd.DataFrame({
    'order_id': [1, 2, 3, 4, 5],
    'city': ['Ahmedabad', 'Surat', 'Rajkot', 'Mumbai', 'Pune'],
    'delivery_days': [2, 5, 1, 7, 4]
})

# A. .isin(): Cleanly filters against a list (replaces multiple 'or' conditions)
gujarat_orders = orders[orders['city'].isin(['Ahmedabad', 'Surat', 'Rajkot'])]
print("Filtered via .isin() (Gujarat Only):")
print(gujarat_orders[['order_id', 'city']])

# B. .between(): Inclusive numerical range filter (replaces '>= 2 & <= 5')
standard_delivery = orders[orders['delivery_days'].between(2, 5)]
print("\nFiltered via .between(2, 5) Days:")
print(standard_delivery[['order_id', 'delivery_days']])


# =====================================================================
# 5. DEDUPLICATION & VALUE MAPPING
# =====================================================================
print("\n--- 5. DEDUPLICATION & MAPPING ---")

raw_leads = pd.DataFrame({
    'email': ['test@gmail.com', 'client@yahoo.com', 'test@gmail.com', 'info@corp.in'],
    'status_code': [1, 2, 1, 3]
})

# A. .drop_duplicates(): Keeps the first occurrence and purges redundant data
clean_leads = raw_leads.drop_duplicates(subset=['email'], keep='first').copy()
print("Deduplicated Leads:")
print(clean_leads)

# B. .map(): Replaces numerical codes with readable business labels
status_dict = {1: 'New Lead', 2: 'Contacted', 3: 'Converted'}
clean_leads['status_label'] = clean_leads['status_code'].map(status_dict)
print("\nMapped Status Codes:")
print(clean_leads[['email', 'status_label']])