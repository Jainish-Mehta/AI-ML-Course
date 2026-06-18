import numpy as np
from scipy import stats

def calculate_correlations(features: dict, target: np.ndarray, target_name: str = "target"):
    """Computes and prints Pearson correlation coefficients for a dictionary of features."""
    print(f"--- Correlation Analysis vs {target_name} ---")
    
    for name, data in features.items():
        r_value = np.corrcoef(data, target)[0, 1]
        print(f"{name:<20} : {r_value:.4f}")

def run_ttest(control: np.ndarray, test: np.ndarray, alpha: float = 0.05):
    """Executes Welch's t-test and determines statistical significance."""
    print("\n--- Independent T-Test Results ---")
    
    t_stat, p_value = stats.ttest_ind(control, test, equal_var=False)
    
    print(f"Control Mean : {np.mean(control):.2f}")
    print(f"Test Mean    : {np.mean(test):.2f}")
    print(f"T-Statistic  : {t_stat:.4f}")
    print(f"P-Value      : {p_value:.6f}")
    
    if p_value < alpha:
        print(f"Conclusion   : Statistically significant (Reject H0, p < {alpha})")
    else:
        print(f"Conclusion   : Not significant (Fail to reject H0, p >= {alpha})")

if __name__ == "__main__":
    features_dict = {
        "Square_Footage": np.array([1000, 1500, 2000, 2500, 3000]),
        "Age_Years": np.array([50, 40, 30, 10, 5]),
        "Distance_Miles": np.array([5, 10, 15, 20, 25])
    }
    target_prices = np.array([150, 220, 280, 360, 410])
    
    control_sales = np.array([20, 25, 22, 19, 28, 24, 21, 26, 23, 20])
    test_sales = np.array([30, 28, 35, 32, 29, 31, 34, 27, 33, 30])
    
    calculate_correlations(features_dict, target_prices, target_name="House_Price")
    run_ttest(control_sales, test_sales)