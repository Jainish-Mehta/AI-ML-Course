import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

current_dir = Path(__file__).resolve().parent.parent.parent
def plot_adaptive_curve(X_features, y_prices, bias, w1, w2):
    """Renders the Matplotlib dashboard showing the Polynomial Curve."""
    print("\n📈 Plotting Adaptive AI trajectory...")
    
    plt.figure(figsize=(10, 6))
    
    plt.scatter(X_features, y_prices, color='red', s=80, edgecolor='black', label='Actual Sales (Ground Truth)')

    x_smooth = np.linspace(X_features.min(), X_features.max(), 100)
    y_smooth = bias + (w1 * x_smooth) + (w2 * (x_smooth ** 2))
    
    plt.plot(x_smooth, y_smooth, color='blue', linewidth=3, label='AI Polynomial Model')

    
    plt.title("MLOps Telemetry: Adaptive Real Estate Model", fontsize=16, fontweight='bold')
    plt.xlabel("Square Footage (x1000)", fontsize=12)
    plt.ylabel("Price ($1000s)", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.savefig(current_dir / "data"/ "prediction" / "Prediction_Chart.png")
    
    plt.show()