import numpy as np
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))
from src.advanced_property_price_prediction.advanced_property_prediction import AHMEDABAD_REGIONS

ZONES_LIST = list(AHMEDABAD_REGIONS.keys())

def encode_locations(loc_list):
    encoded = []
    for loc in loc_list:
        row = [0] * len(ZONES_LIST)
        if loc in ZONES_LIST:
            index = ZONES_LIST.index(loc)
            row[index] = 1
        encoded.append(row)
    return np.array(encoded)

def standardize_features(num_features, means=None, stds=None):
    if means is None or stds is None:
        means = np.mean(num_features, axis=0)
        stds = np.std(num_features, axis=0, ddof=1)
        stds[stds == 0] = 1e-8 
    z_scores = (num_features - means) / stds
    return z_scores, means, stds

def train_multiple_regression(num_features, loc_list, y_prices):
    # 🛑 PRO TRICK: Inject SqFt^2 into the features so the AI can learn curves!
    sqft_squared = (num_features[:, 0] ** 2).reshape(-1, 1)
    enhanced_features = np.hstack((num_features, sqft_squared))
    
    X_scaled, means, stds = standardize_features(enhanced_features)
    X_cat = encode_locations(loc_list)
    
    bias = np.ones((len(X_scaled), 1))
    X_final = np.hstack((bias, X_scaled, X_cat))
    
    X_T = X_final.T
    weights = np.linalg.pinv(X_T @ X_final) @ X_T @ y_prices
    return weights, means, stds

def predict_price(new_num_features, new_loc, weights, means, stds):
    # new_num_features comes in as [sqft, beds, age]
    # We must add sqft^2 to match the training architecture!
    sqft = new_num_features[0]
    enhanced_input = np.array([new_num_features + [sqft**2]])
    
    scaled_input, _, _ = standardize_features(enhanced_input, means, stds)
    cat_input = encode_locations([new_loc])
    
    x_vector = np.hstack(([1.0], scaled_input[0], cat_input[0]))
    return np.dot(x_vector, weights)