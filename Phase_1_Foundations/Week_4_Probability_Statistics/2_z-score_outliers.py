import numpy as np

print("--- 🕵️ AUTOMATED OUTLIER DETECTION (Z-SCORES) ---")

transactions = np.array([25, 30, 45, 20, 50, 60, 40, 35, 900, 55, 30, 1200, 45, 65])

mean_tx = np.mean(transactions)
std_tx = np.std(transactions)
print(f"Dataset Mean: ${mean_tx:.2f} | Standard Deviation: ${std_tx:.2f}\n")

z_scores = (transactions - mean_tx) / std_tx

outlier_threshold = 2.5 
outlier_mask = np.abs(z_scores) > outlier_threshold

outliers = transactions[outlier_mask]
normal_data = transactions[~outlier_mask] # The ~ symbol means "NOT" (Invert the mask)

print(f" FRAUD DETECTED! Outlier Transactions: {outliers}")
print(f" Normal Transactions: {normal_data}\n")


print("--- ⚖️ FEATURE SCALING (Standardization for Neural Networks) ---")

print("Raw Data (Dollars):")
print(transactions)

print("\nStandardized Data (Z-Scores):")
print(np.round(z_scores, 2))

scaled_mean = np.mean(z_scores)
scaled_std = np.std(z_scores)

print(f"\nProof -> Scaled Mean: {scaled_mean:.10f} (Basically 0)")
print(f"Proof -> Scaled Std Dev: {scaled_std:.2f} (Exactly 1)")