import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

root = Path(__file__).resolve().parent.parent
parquet_file = root / "data" / "india_transactions.parquet"
dashboard_output = root / "data" / "india_executive_dashboard.png"

def render_dashboard():
    print("⚙️ Loading 1-Million Row Parquet File into RAM...")
    if not parquet_file.exists():
        print("❌ Parquet file not found! Run financial_etl.py first.")
        return

    df = pd.read_parquet(parquet_file, engine='pyarrow')
    print("✅ Data Loaded. Rendering Executive Dashboard...")

    sns.set_theme(style="whitegrid")
    fig = plt.figure(figsize=(16, 10))
    
    # --- PLOT 1: Total Revenue by State (Top Left) ---
    ax1 = plt.subplot(2, 2, 1)
    state_revenue = df.groupby('state_code', observed=True)['amount_inr'].sum().reset_index()
    state_revenue = state_revenue.sort_values(by='amount_inr', ascending=False)
    
    # Map State Codes to Full Names for the graph
    state_mapping = {'MH': 'Maharashtra', 'KA': 'Karnataka', 'DL': 'Delhi', 'GJ': 'Gujarat', 'TN': 'Tamil Nadu'}
    state_revenue['state_name'] = state_revenue['state_code'].map(state_mapping)

    sns.barplot(data=state_revenue, x='state_name', y='amount_inr', hue='state_name', palette='magma', ax=ax1, legend=False)
    ax1.set_title("Total Transaction Volume by State", fontsize=14, fontweight='bold')
    ax1.set_ylabel("Total Volume (₹ Crores)")
    ax1.set_xlabel("")
    
    # 🛑 INDIAN FINANCE FORMATTING: Convert raw Rupees to Crores (1 Crore = 10,000,000)
    ax1.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: f"₹{x/10000000:.1f} Cr"))

    # --- PLOT 2: High Risk vs Standard Distribution (Top Right) ---
    ax2 = plt.subplot(2, 2, 2)
    risk_counts = df['risk_flag'].value_counts()
    
    ax2.pie(risk_counts, labels=risk_counts.index, autopct='%1.1f%%', 
            startangle=90, colors=['#3498db', '#e74c3c'], explode=(0, 0.1))
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    ax2.add_artist(centre_circle)
    ax2.set_title("RBI Compliance Risk Distribution", fontsize=14, fontweight='bold')

    # --- PLOT 3: Transaction Amount Distribution (Bottom Wide) ---
    ax3 = plt.subplot(2, 1, 2)
    sns.histplot(data=df, x='amount_inr', bins=50, color='#2ecc71', kde=True, ax=ax3)
    
    # 🛑 THRESHOLD LINE: 5 Lakhs
    ax3.axvline(x=500000, color='red', linestyle='--', linewidth=2, label="Risk Threshold (₹5 Lakhs)")
    
    ax3.set_title("Transaction Value Density Distribution", fontsize=14, fontweight='bold')
    ax3.set_ylabel("Number of Transactions")
    ax3.set_xlabel("Transaction Amount (INR)")
    ax3.legend()
    
    # Format X-axis in Lakhs (1 Lakh = 100,000)
    ax3.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: f"₹{x/100000:.0f}L"))

    # --- FINAL FORMATTING & EXPORT ---
    fig.suptitle("Indian Fintech Overview (1,000,000 Processed Transactions)", 
                 fontsize=20, fontweight='heavy', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(dashboard_output, dpi=300)
    print(f"📸 Dashboard saved securely to: {dashboard_output.name}")
    plt.show()

if __name__ == "__main__":
    render_dashboard()