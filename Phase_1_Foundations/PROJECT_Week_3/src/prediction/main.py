import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import models.prediction.property_price_predictor as model
import visualize

def main():
    print("--- MLOPS ADAPTIVE AI ENGINE ---")
    
    model.init_db()
    
    while True:
        X_features, y_prices = model.get_training_data()
        bias, w1, w2 = model.train_polynomial_model(X_features, y_prices)
        
        print(f"\n[Database Records: {len(X_features)}] | Formula: Price = {bias:.2f} + ({w1:.2f}*X) + ({w2:.2f}*X^2)")
        
        try:
            user_input = input("\nEnter new house SqFt (e.g., 2.8) or 'q' to quit: ")
            if user_input.lower() == 'q':
                break
                
            new_sqft = float(user_input)
            
            predicted_price = bias + (w1 * new_sqft) + (w2 * (new_sqft ** 2))
            print(f"AI Predicts: ${predicted_price * 1000:,.2f}")
            
            actual_price = float(input("What did it ACTUALLY sell for? (e.g., 380): "))
            model.log_telemetry(new_sqft, predicted_price, actual_price)
            
            print("Telemetry Logged! AI will retrain on the next loop.")
                
        except ValueError:
            print("Please enter valid numbers.")

    visualize.plot_adaptive_curve(X_features, y_prices, bias, w1, w2)

if __name__ == "__main__":
    main()