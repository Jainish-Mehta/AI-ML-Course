import numpy as np
print("="*50 +"Scalar Example"+"="*50)
scalar = np.array(5)
print(f"Dimension: {scalar.ndim}D | Shape: {scalar.shape} | Value: {scalar}")

print("\n"+"="*50+"Vector Example"+"="*50)
vector = np.array([10,20,30,40,50])
print(f"Dimension: {vector.ndim}D | Shape: {vector.shape} | Value: {vector}")

print("\n"+"="*50+"Matrix Example"+"="*50)
matrix = np.array([[1,2,3],[4,5,6],[7,8,9]])
print(f"Dimension: {matrix.ndim}D | Shape: {matrix.shape} | Value:\n{matrix}")

print("\n"+"="*50+"3D Example"+"="*50)
tensor = np.array([[[1,2],[3,4]],[[5,6],[7,8]]])
print(f"Dimension: {tensor.ndim}D | Shape: {tensor.shape} | Value:\n{tensor}")