import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set visual style
sns.set_theme(style="whitegrid")

# ==========================================
# 1. LOAD DATA
# ==========================================
print("Loading dataset...")
# Make sure your CSV file is named 'semiconductor_data_full.csv'
df = pd.read_csv('semiconductor_data_full.csv')

# 1.1 Column Mapping
# Map your specific LSEG headers to standard variable names
rename_map = {
    'Instrument': 'Ticker',
    'Company': 'Company',
    'YTD Price PCT Change': 'YTD_Return', # Mapping the Momentum column
    # These match your CSV exactly, but good to be explicit
    'Market_Cap': 'Market_Cap', 
    'Revenue': 'Revenue',
    'EBITDA': 'EBITDA',
    'R&D_Expense': 'R&D_Expense'
}
df = df.rename(columns=rename_map)

# Drop any rows where critical data is missing
df = df.dropna(subset=['EBITDA', 'Revenue', 'YTD_Return'])

print(f"✅ Loaded {len(df)} companies.")

# ==========================================
# 2. FEATURE ENGINEERING
# ==========================================
print("Calculating Factors...")

# 2.1 Valuation Factor (Lower is Better)
# Proxy for EV/EBITDA
df['Valuation_Multiple'] = df['Market_Cap'] / df['EBITDA']

# 2.2 Innovation Factor (Higher is Better)
# R&D Intensity = R&D / Revenue
df['R&D_Intensity'] = df['R&D_Expense'] / df['Revenue']

# 2.3 Momentum Factor (Higher is Better)
# Already have YTD_Return

# ==========================================
# 3. Z-SCORE SCORING ENGINE
# ==========================================
def calculate_z_score(series):
    # Standardize data to Mean=0, Std=1
    return (series - series.mean()) / series.std()

# 3.1 Calculate Z-Scores
# INVERT Valuation because Lower is Better (Cheaper)
df['Z_Valuation'] = -1 * calculate_z_score(df['Valuation_Multiple'])
df['Z_Innovation'] = calculate_z_score(df['R&D_Intensity'])
df['Z_Momentum'] = calculate_z_score(df['YTD_Return'])

# 3.2 Composite Score Construction
# Strategy: "Balanced Tech Quant"
# 40% Innovation (It's semi, tech is king)
# 30% Valuation (Don't overpay)
# 30% Momentum (Ride the trend)
df['Final_Score'] = (
    0.4 * df['Z_Innovation'] +
    0.3 * df['Z_Valuation'] +
    0.3 * df['Z_Momentum']
)

# 3.3 Normalization (0-100 Scale)
min_score = df['Final_Score'].min()
max_score = df['Final_Score'].max()
df['Score_0_100'] = ((df['Final_Score'] - min_score) / (max_score - min_score)) * 100

# ==========================================
# 4. RANKING & OUTPUT
# ==========================================
# Sort by Score
df = df.sort_values(by='Score_0_100', ascending=False)
df['Rank'] = range(1, len(df) + 1)

# Formatting for nice display
df['Valuation_Display'] = df['Valuation_Multiple'].map('{:.1f}x'.format)
df['RD_Display'] = df['R&D_Intensity'].map('{:.1%}'.format)
df['YTD_Display'] = df['YTD_Return'].map('{:.1f}%'.format)

print("TOP 5 SEMICONDUCTOR RANKING:")
print(df[['Rank', 'Ticker', 'Company', 'Score_0_100', 'Valuation_Display', 'RD_Display', 'YTD_Display']].head().to_string(index=False))

# Save Results
df.to_csv('final_ranking.csv', index=False)

# ==========================================
# 5. VISUALIZATION (For GitHub)
# ==========================================
plt.figure(figsize=(12, 8))
chart = sns.barplot(x='Score_0_100', y='Company', data=df, palette='viridis')

plt.title('Global Semiconductor Quant Strategy: 3-Factor Model (2025)', fontsize=14, pad=20)
plt.xlabel('Composite Score (Innovation + Value + Momentum)', fontsize=12)
plt.ylabel('')
plt.axvline(x=50, color='grey', linestyle='--', alpha=0.5)

# Add score labels
for i in chart.containers:
    chart.bar_label(i, fmt='%.1f', padding=5)

plt.tight_layout()
plt.savefig('quant_ranking_chart.png', dpi=300)