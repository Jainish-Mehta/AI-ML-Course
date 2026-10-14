import numpy as np

print("--- 1. CENTRAL TENDENCY (The Middle) ---")
incomes = np.array([30, 32, 35, 38, 40, 42, 45, 48, 50, 950])

mean_income = np.mean(incomes)
median_income = np.median(incomes)
#for mode use np.argmax(np.bincount(incomes))

print(f"Data: {incomes}")
print(f"Mean (Average): {mean_income}k  <-- (Misleading because of the 950k CEO!)")
print(f"Median (Middle): {median_income}k  <-- (A much better representation)")


print("\n--- 2. SPREAD & DISPERSION (The Chaos) ---")
machine_A = np.array([99, 100, 101, 100, 99, 101])
machine_B = np.array([80, 120, 70, 130, 60, 140])

std_A = np.std(machine_A)
std_B = np.std(machine_B)

print(f"Machine A Std Dev: {std_A:.2f}mm (Very consistent!)")
print(f"Machine B Std Dev: {std_B:.2f}mm (Chaotic. The machine is broken!)")
# variance is std square
variance_A = np.var(machine_A)
variance_B = np.var(machine_B)
print(f"Machine A Variance: {variance_A:.2f}mm²")
print(f"Machine B Variance: {variance_B:.2f}mm²")

print("\n--- 3. PERCENTILES & IQR (Interquartile Range) ---")
scores = np.array([45, 55, 65, 75, 80, 85, 90, 95, 99, 100])

Q1 = np.percentile(scores, 25)
Q3 = np.percentile(scores, 75)

IQR = Q3 - Q1

print(f"Test Scores: {scores}")
print(f"Bottom 25% boundary (Q1): {Q1}")
print(f"Top 25% boundary (Q3): {Q3}")
print(f"The Middle 50% of students scored within an IQR range of: {IQR} points")