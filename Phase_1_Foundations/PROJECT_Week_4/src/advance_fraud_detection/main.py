import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

import db_handler
from models.advance_fraud_detection import stats_model

def main():
    print("--- 🛡️ ENTERPRISE A/B TEST & FRAUD ENGINE ---")
    
    db_handler.initialize_and_seed_db()
    print("[SYSTEM] Database seeded with 1,000 transactions (Includes hidden fraud).")
    
    raw_A = db_handler.fetch_group_data("A")
    raw_B = db_handler.fetch_group_data("B")
    
    print("\n--- 🛑 PHASE 1: THE RAW DATA (POISONED) ---")
    print(f"Group A Raw Mean: ${np.mean(raw_A):,.2f}")
    print(f"Group B Raw Mean: ${np.mean(raw_B):,.2f}")
    print("Warning: If we stop here, the boss will choose Group A!")
    
    print("\n--- 🧹 PHASE 2: STATISTICAL FILTRATION (Z-SCORES) ---")
    clean_A, outliers_A = stats_model.remove_outliers_zscores(raw_A, threshold=3.0)
    clean_B, outliers_B = stats_model.remove_outliers_zscores(raw_B, threshold=3.0)
    
    print(f"Group A Outliers Removed: {len(outliers_A)} (Values: {outliers_A})")
    print(f"Group B Outliers Removed: {len(outliers_B)}")
    print(f"Group A Clean Mean: ${np.mean(clean_A):,.2f}")
    print(f"Group B Clean Mean: ${np.mean(clean_B):,.2f}")
    
    print("\n--- ⚖️ PHASE 3: WELCH'S T-TEST ---")
    t_stat, p_value, is_sig = stats_model.run_welchs_ttest(clean_A, clean_B)
    
    print(f"P-Value: {p_value:.6f}")
    if is_sig:
        print("✅ RESULT: Statistically Significant! Group B is genuinely better.")
    else:
        print("❌ RESULT: Not Significant. The variance is stochastic noise.")
        
    print("\n📈 Rendering Statistical Boxplots...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    ax1.boxplot([raw_A, raw_B], labels=['Group A', 'Group B'])
    ax1.set_title("Raw Data (Notice the $15,000 Outliers in A!)", fontweight='bold')
    ax1.set_ylabel("Transaction Amount ($)")
    ax1.grid(True, alpha=0.3)
    
    ax2.boxplot([clean_A, clean_B], labels=['Group A', 'Group B'])
    ax2.set_title("Cleaned Data (Z-Score Filtered)", fontweight='bold')
    ax2.set_ylabel("Transaction Amount ($)")
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(project_root/"data"/"advance_fraud_detection"/"fraud_chart.png")
    plt.show()

if __name__ == "__main__":
    main()