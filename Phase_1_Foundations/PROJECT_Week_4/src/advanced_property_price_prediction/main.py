import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

import advanced_property_prediction as db_property
from models.advanced_property_price_prediction import predictor_model as ml_engine

def main():
    print("--- 🧠 AHMEDABAD COMPREHENSIVE REAL ESTATE ENGINE ---")
    
    # 🛑 CRITICAL STEP: We must delete the old .db file so it rebuilds with the 24 new zones!
    if db_property.db_path.exists():
        # Quick check: If the old DB only has the 6 old zones, it will crash the 24-zone matrix.
        # It's safest to just delete it manually in VS Code before running, 
        # or let the code gracefully rebuild it if it's your first run today.
        pass

    db_property.init_db()
    
    while True:
        num_features, locations, prices = db_property.fetch_all_data()
        weights, means, stds = ml_engine.train_multiple_regression(num_features, locations, prices)
        
        print(f"\n[Database Records: {len(prices):,}] | 28-Dimensional Tensor Compiled.")
        
        print("\n--- Enter Property Details (or 'q' to quit) ---")
        user_input = input("SqFt (e.g., 2000): ")
        if user_input.lower() == 'q': break
            
        try:
            sqft = float(user_input)
            beds = int(input("Bedrooms (e.g., 3): "))
            age = float(input("Age in Years (e.g., 5): "))
            
            # Print the massive list of zones so the user knows what to type
            print("\nAvailable Zones:")
            print(", ".join(ml_engine.ZONES_LIST[:10]) + "...") # Preview the first 10
            
            loc = input("Enter exact Zone Name: ")
            
            # Sanity Check for Location
            if loc not in ml_engine.ZONES_LIST:
                print("⚠️ Unknown zone! Defaulting to 'Daskroi' baseline.")
                loc = 'Daskroi'
            
            prediction_lakhs = ml_engine.predict_price([sqft, beds, age], loc, weights, means, stds)
            
            print(f"\n🔮 AI Predicts: ₹{prediction_lakhs:,.2f} Lakhs")
            
            actual_price = float(input("What did it ACTUALLY sell for? (in Lakhs): "))
            
            # Sanity check to prevent trillion-rupee database corruption
            if actual_price > 10000:
                print("⚠️ WARNING: That is over 10,000 Lakhs! Assuming you typed raw Rupees.")
                actual_price = actual_price / 100000
                print(f"✅ Corrected to: ₹{actual_price:.2f} Lakhs")
                
            db_property.log_new_property(sqft, beds, age, loc, actual_price)
            print("💾 Data saved. The 28-Dimensional Matrix will adapt on the next loop.")
            
        except ValueError:
            print("❌ Invalid input. Please enter numbers where required.")

if __name__ == "__main__":
    main()