import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pathlib import Path
import sys

# Dynamic routing
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

import advanced_property_prediction as db_property
from models.advanced_property_price_prediction import predictor_model as ml_engine

def render_combined_ai_chart():
    print("⚙️ Loading Data and Compiling AI Matrix...")
    
    # 1. Fetch Data & Train the AI
    num_features, locations, prices = db_property.fetch_all_data()
    weights, means, stds = ml_engine.train_multiple_regression(num_features, locations, prices)
    
    # We load Pandas just to get the list of unique zones actually present in the DB
    df = pd.DataFrame({'sqft': num_features[:, 0], 'price': prices, 'loc': locations})
    unique_zones = df['loc'].unique()

    print(f"📊 Rendering Combined AI Model Curve for {len(unique_zones)} Zones...")

    # 2. Setup the Single Giant Chart
    plt.figure(figsize=(16, 9))
    
    # Plot the raw data lightly in the background so it doesn't distract from the curves
    plt.scatter(df['sqft'], df['price'], color='lightgray', alpha=0.3, s=10, label='Raw Data points')

    # Get a colormap to automatically assign different colors to our lines
    colors = cm.get_cmap('tab20', len(unique_zones))

    # 3. Generate the AI Curve for each zone
    # We ask the AI to predict prices for houses from 800 to 5000 sqft
    sqft_range = np.linspace(800, 5000, 100)
    
    # We hold Beds and Age constant to isolate the SqFt vs Price curve
    assumed_beds = 3
    assumed_age = 5.0

    for i, zone in enumerate(unique_zones):
        predicted_prices = []
        
        # Make the AI predict the price for every point on the line
        for sqft in sqft_range:
            price = ml_engine.predict_price([sqft, assumed_beds, assumed_age], zone, weights, means, stds)
            predicted_prices.append(price)
            
        # Draw the curved line for this zone!
        plt.plot(sqft_range, predicted_prices, color=colors(i), linewidth=2.5, label=zone)

    # 4. Formatting
    plt.title("AI Pricing Model: Polynomial Curves by Zone (3 Beds, 5 Yrs Old)", fontsize=18, fontweight='bold')
    plt.xlabel("Square Footage", fontsize=14)
    plt.ylabel("Predicted Price (Lakhs ₹)", fontsize=14)
    
    # Put the legend outside the chart so it doesn't block the lines
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10, title="Ahmedabad Zones")
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    print("📈 Displaying Graph...")
    plt.savefig(project_root / "data" / "advanced_property_price_prediction" / "property_prices.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    render_combined_ai_chart()