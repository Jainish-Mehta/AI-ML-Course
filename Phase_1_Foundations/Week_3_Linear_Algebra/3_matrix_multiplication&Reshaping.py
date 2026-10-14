import numpy as np

print("="*50 +"Matrix Multiplication Example"+"="*50)

m3x2 = np.array([
    [2,4],
    [1,5],
    [6,3]
])

m2x1 = np.array([
    [2.0],
    [1.25]
])

print(f"\nMatrix3x2 Shape: {m3x2.shape} | Value:\n{m3x2}")
print(f"\nMatrix2x1 Shape: {m2x1.shape} | Value:\n{m2x1}")

if m3x2.shape[1] == m2x1.shape[0]:
    result = m3x2 @ m2x1
    print(f"\nResult of Matrix Multiplication: {result}")
    
m1x2 = np.array([
    [2.0,1.25]
])

print(f"\nMatrix1x2 Shape: {m1x2.shape} | Value:\n{m1x2}")
transformed_matrix = m1x2.T # now m1x2 becomes m2x1

if m3x2.shape[1] == transformed_matrix.shape[0]:
    result = m3x2 @ transformed_matrix
    print(f"\nResult using transformed Matrix: {result}")

print("\n"+"="*50+"Reshaping Example"+"="*50)

matrix = np.array([
    [12,12],[10,10]
])

reshaped_matrix = matrix.reshape(-1)
print(f"\nReshaped Matrix Shape: {reshaped_matrix.shape} | Value: \n{reshaped_matrix}")