import eikon as ek
import pandas as pd

# ==========================================
# 1. API CONNECTION
# ==========================================
# Connect to LSEG Workspace (Refinitiv Eikon).
# NOTE: Replace 'YOUR_APP_KEY_HERE' with your actual generated App Key before running.
# DO NOT upload your real key to GitHub.
ek.set_app_key('YOUR_APP_KEY_HERE') 

print("⏳ Connecting to LSEG... Fetching Historical Prices for Volatility Analysis...")

# ==========================================
# 2. UNIVERSE DEFINITION
# ==========================================
# The same 15-stock universe used in the fundamental scoring model.
tickers = [
    'NVDA.O', 'AMD.O', 'TSM.N', 'ASML.O', '0981.HK', 
    'MU.O', 'QCOM.O', 'AVGO.O', 'LRCX.O', 'AMAT.O',
    'TXN.O', 'ADI.O', 'INTC.O', 'GFS.O'
]

# ==========================================
# 3. FETCH TIME-SERIES DATA
# ==========================================
try:
    # Use 'get_timeseries' to retrieve daily closing prices.
    # We need historical data to calculate the Covariance Matrix for Markowitz Optimization.
    prices = ek.get_timeseries(
        tickers, 
        fields='CLOSE', 
        start_date='2024-01-01',  # Start of analysis period
        end_date='2025-12-04',    # Current date
        interval='daily'
    )
    
    # ==========================================
    # 4. INSPECT & SAVE
    # ==========================================
    print(f"✅ Data Fetched Successfully. Shape: {prices.shape}")
    print("\nPreview of Price Data:")
    print(prices.head())
    
    # Save to CSV for the Portfolio Optimization script
    output_file = 'semiconductor_price_history.csv'
    prices.to_csv(output_file)
    print(f"\n📁 Historical prices saved to '{output_file}'")

except Exception as e:
    print(f" Error fetching historical data: {e}")
    print("Tip: Ensure your LSEG Desktop App is running.")