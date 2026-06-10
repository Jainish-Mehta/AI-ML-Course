import time
import subprocess
from pathlib import Path
from datetime import datetime

script_to_run = Path(__file__).resolve().parent / "crypto_logs.py"

TOTAL_RUNS = 10
SLEEP_INTERVAL_SECONDS = 60  

print("🚀 Starting Automated Data Pipeline...")
print(f"Goal: {TOTAL_RUNS} Extractions | Interval: {SLEEP_INTERVAL_SECONDS} seconds.\n")

for i in range(1, TOTAL_RUNS + 1):
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"--- [RUN {i}/{TOTAL_RUNS}] Executing at {current_time} ---")
    
    try:
        subprocess.run(["python", str(script_to_run)], check=True)
        print(f"✅ Run {i} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during execution: {e}")
        break 
    
    if i < TOTAL_RUNS:
        print(f"💤 Sleeping for {SLEEP_INTERVAL_SECONDS} seconds...\n")
        time.sleep(SLEEP_INTERVAL_SECONDS)

print("\n🏁 Automation Complete! You now have 10 new data points.")
print("Go run 'visualize_db.py' to see your new graph!")

visulaize_script = Path(__file__).resolve().parent / "crypto_visualization.py"
print(f"\nCreating visualization using '{visulaize_script.name}'...")
try:
    subprocess.run(["python", str(visulaize_script)], check=True)
    print("📊 Visualization created successfully.")
except subprocess.CalledProcessError as e:
    print(f"❌ Error during visualization: {e}")
    