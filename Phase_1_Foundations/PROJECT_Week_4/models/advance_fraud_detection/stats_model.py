import numpy as np
from scipy import stats

def remove_outliers_zscores(data_array, threshold=3.0):
    mean_val = np.mean(data_array)
    std_val = np.std(data_array, ddof=1)
    
    z_scores = (data_array - mean_val) / std_val
    
    normal_mask = np.abs(z_scores) <= threshold
    outlier_mask = np.abs(z_scores) > threshold
    
    clean_data = data_array[normal_mask]
    outliers = data_array[outlier_mask]
    
    return clean_data, outliers

def run_welchs_ttest(control_data, test_data, alpha=0.05):
    t_stats, p_value = stats.ttest_ind(control_data, test_data, equal_var=False)
    is_significant = p_value < alpha
    
    return t_stats, p_value, is_significant