import numpy as np

print("="*50+"Vectorization Eample"+"="*50)
old_prices = np.array([10,20,30,40,50])
new_prices = old_prices + 5
print(f"\nOLD Prices: {old_prices}\nNEW Prices: {new_prices}")

print("="*50+"Broadcasting Example"+"="*50)
matrix = np.array([[1,2,3],[4,5,6],[7,8,9]])
vector = np.array([10,20,30])
 # This will be added to each row of the matrix. 
 # Note:- Different Dimensions can be combined together if their shapes are same

result = matrix + vector
print(f"\nDimension: {result.ndim} | Shape: {result.shape} | Value: \n{result}")

print("\n"+"="*50+"Dot Product Example"+"="*50)
quantities = np.array([1,2,5])
prices = np.array([10,20,30])
calculations = quantities * prices
result = np.dot(quantities,prices)
print(f"\nQuantities: {quantities}\nPrices: {prices} \nCalculation: {calculations} \nTotal Cost (Dot Product): {result}")