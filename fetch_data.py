import eikon as ek
import pandas as pd
import os

# ==========================================
# 1. API CONNECTION
# ==========================================
# I've embedded your key. 
ek.set_app_key('YOUR_APP_KEY_HERE')

# ==========================================
# 2. UNIVERSE
# ==========================================
tickers = [
    'NVDA.O', 'AMD.O', 'TSM.N', 'ASML.O', '0981.HK', 
    'MU.O', 'QCOM.O', 'AVGO.O', 'LRCX.O', 'AMAT.O',
    'TXN.O', 'ADI.O', 'INTC.O', 'GFS.O'
]

# ==========================================
# 3. FIELDS (The Fix is Here)
# ==========================================
# We use TR.ResearchAndDevelopment because we know it works.
fields = [
    'TR.CommonName',
    'TR.PriceClose',
    'TR.CompanyMarketCap',
    'TR.TotalRevenue',
    'TR.EBITDA',
    'TR.ResearchAndDevelopment',     # <--- REVERTED TO THE WORKING FIELD
    'TR.GrossProfitMargin',
    'TR.ReturnOnInvestedCapital',
    'TR.PricePctChgYTD'
]

# ==========================================
# 4. PARAMETERS
# ==========================================
# Applying LTM and USD globally to avoid syntax errors
params = {
    'Period': 'LTM', 
    'Curn': 'USD',
    'Scale': '6'
}

try:
    df, err = ek.get_data(tickers, fields, parameters=params)

    # Error Check
    if err is not None:
        print("--- API WARNINGS ---")
        print(err)

    # ==========================================
    # 5. RENAME & CLEAN
    # ==========================================
    # Debug: Print columns to confirm what we got
    # print("Columns returned:", df.columns.tolist())

    df = df.rename(columns={
        'Company Market Cap': 'Market_Cap',
        'Total Revenue': 'Revenue',
        'EBITDA': 'EBITDA',
        
        # This matches TR.ResearchAndDevelopment output
        'Research And Development': 'R&D_Expense', 
        
        'Gross Profit Margin': 'Gross_Margin',
        'Return on Invested Capital': 'ROIC',
        'Price PCT Change YTD': 'YTD_Return',
        'Price Close': 'Price',
        'Company Common Name': 'Company'
    })

    # Drop rows only if essential valuation data is missing
    df = df.dropna(subset=['Revenue', 'EBITDA'])

    # Fill R&D with 0 if missing (so we don't lose the row)
    if 'R&D_Expense' in df.columns:
        df['R&D_Expense'] = df['R&D_Expense'].fillna(0)

    print(f"Success! Extracted data for {len(df)} companies.")
    print("Preview (Look for R&D_Expense column):")
    print(df.head())
    
    # Save raw data
    df.to_csv('semiconductor_data_full.csv', index=False)

except Exception as e:
    print("CRITICAL ERROR:", e)

