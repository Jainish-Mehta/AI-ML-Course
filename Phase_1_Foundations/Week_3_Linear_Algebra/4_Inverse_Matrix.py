import numpy as np

print("="*50+"Inverse Matrix Example"+"="*50)
identity_matrix = np.eye(3)
print(f"Identity Matrix:\n{identity_matrix}")

random_matrix = np.array([
    [10,20,30],
    [40,50,60],
    [70,80,90]
])

result = random_matrix @ identity_matrix
print(f"Result of Matrix Multiplication:\n{result}")

print("="*50+"Inverse Matrix Example"+"="*50)

matrix = np.array([
    [2,4],
    [1,5]
])

print(f"Original Matrix:\n{matrix}")

inverse_matrix = np.linalg.inv(matrix)
print(f"Inverse Matrix:\n{inverse_matrix}")

print("="*50+"Proof"+"="*50)
proof =np.round(matrix @ inverse_matrix)
print(f"Proof (should be Identity Matrix):\n{proof}")