import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path

# Paths
root = Path(__file__).resolve().parent
data_dir = root / "data"
output_plot = data_dir / "univariate_transformation.png"

def run_univariate_diagnostics():
    print("--- 📊 UNIVARIATE DISTRIBUTION & SKEWNESS DIAGNOSTICS ---\n")
    
    # 1. GENERATE HEAVILY SKEWED DATA (e.g., Annual Incomes in Lakhs)
    # Lognormal distribution creates a realistic long-tailed economic dataset
    np.random.seed(42)
    raw_incomes = np.random.lognormal(mean=2.5, sigma=1.0, size=5000)
    
    df = pd.DataFrame({"income_lakhs": raw_incomes})

    # 2. COMPUTE STATISTICAL MOMENTS (Raw Data)
    # Skewness: 0 = Symmetric, > 1 = Heavily Right-Skewed, < -1 = Heavily Left-Skewed
    # Kurtosis: Measures tail-heaviness / outlier propensity (Normal distribution = 3, Fisher's = 0)
    raw_skew = stats.skew(df["income_lakhs"])
    raw_kurt = stats.kurtosis(df["income_lakhs"]) # Fisher's definition (0 is normal)

    print(f"[RAW DATA METRICS]")
    print(f"Mean     : ₹{df['income_lakhs'].mean():.2f}L")
    print(f"Median   : ₹{df['income_lakhs'].median():.2f}L")
    print(f"Skewness : {raw_skew:.4f}  (> 1.0 indicates severe positive skew)")
    print(f"Kurtosis : {raw_kurt:.4f}  (High kurtosis indicates heavy outlier tails)")

    # 3. FEATURE ENGINEERING: LOGARITHMIC TRANSFORMATION
    # We use np.log1p(x) which calculates log(1 + x) to safely handle values near 0
    df["income_log"] = np.log1p(df["income_lakhs"])
    
    transformed_skew = stats.skew(df["income_log"])
    transformed_kurt = stats.kurtosis(df["income_log"])

    print(f"\n[TRANSFORMED DATA METRICS (log1p)]")
    print(f"Mean     : {df['income_log'].mean():.2f}")
    print(f"Median   : {df['income_log'].median():.2f}")
    print(f"Skewness : {transformed_skew:.4f}  (Near 0.0 indicates a near-perfect Gaussian distribution)")
    print(f"Kurtosis : {transformed_kurt:.4f}  (Tails stabilized)")

    # 4. VISUAL DIAGNOSTICS (Side-by-Side KDE & QQ-Plots)
    print("\nRendering statistical diagnostic plots...")
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # A. Raw Distribution (Histogram + KDE)
    sns.histplot(df["income_lakhs"], kde=True, color="#e74c3c", ax=axes[0, 0], bins=50)
    axes[0, 0].set_title(f"Raw Income Distribution\nSkew: {raw_skew:.2f} (Extreme Tail)", fontweight="bold")
    axes[0, 0].set_xlabel("Income (Lakhs ₹)")

    # B. Raw Q-Q Plot (Quantile-Quantile Plot compares data to theoretical normal line)
    stats.probplot(df["income_lakhs"], dist="norm", plot=axes[0, 1])
    axes[0, 1].set_title("Raw Q-Q Plot (Heavy deviation from red line)", fontweight="bold")

    # C. Transformed Distribution (Histogram + KDE)
    sns.histplot(df["income_log"], kde=True, color="#2ecc71", ax=axes[1, 0], bins=50)
    axes[1, 0].set_title(f"Transformed Distribution (log1p)\nSkew: {transformed_skew:.2f} (Symmetric Gaussian)", fontweight="bold")
    axes[1, 0].set_xlabel("Log(1 + Income)")

    # D. Transformed Q-Q Plot
    stats.probplot(df["income_log"], dist="norm", plot=axes[1, 1])
    axes[1, 1].set_title("Transformed Q-Q Plot (Data aligns tightly with red line)", fontweight="bold")

    plt.tight_layout()
    plt.savefig(output_plot, dpi=300)
    print(f"✅ Diagnostic dashboard exported to: {output_plot.name}")
    plt.show()

if __name__ == "__main__":
    run_univariate_diagnostics()