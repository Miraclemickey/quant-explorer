# Global Semiconductor Multi-Factor Quant Strategy & Optimization 🌐📊

![Python](https://img.shields.io/badge/Python-3.10-blue) ![Refinitiv](https://img.shields.io/badge/Data-LSEG%20Refinitiv-orange) ![Finance](https://img.shields.io/badge/Strategy-Markowitz%20MPT-green)

## 📌 Executive Summary
This project bridges **Fundamental Analysis** and **Quantitative Modeling** to construct an optimized equity portfolio within the global semiconductor supply chain (US, Taiwan, Hong Kong). 

By leveraging a **3-Factor Scoring Model** (Valuation, Innovation, Momentum) and **Mean-Variance Optimization** (Markowitz), the strategy identifies high-quality assets and allocates capital to maximize the Risk-Adjusted Return (Sharpe Ratio).

## 🛠️ Project Architecture

### 1. Data Engineering (Automated Pipeline)
* **Source:** LSEG Workspace (Refinitiv Eikon) API.
* **Universe:** 15 core semiconductor stocks (e.g., NVDA, TSMC, ASML, SMIC) covering Fabless, Foundry, and Equipment sectors.
* **Normalization:** Dynamic cross-market currency conversion (HKD/TWD to USD) and LTM (Last Twelve Months) alignment.

### 2. Factor Modeling (The "Alpha" Engine)
We constructed a composite Z-Score based on three strategic dimensions:
* **Innovation (40%):** R&D Intensity (R&D Expense / Revenue). Captures long-term technological moats.
* **Valuation (30%):** EV/EBITDA proxy. Identifying mispriced value relative to cash flow.
* **Momentum (30%):** YTD Price Performance. Capturing market sentiment and trend persistence.

### 3. Portfolio Optimization (Risk Management)
Instead of equal weighting, the top fundamental picks were fed into a **Markowitz Mean-Variance Optimizer**:
* **Objective:** Maximize Sharpe Ratio.
* **Constraint:** Individual asset cap of 40% to ensure diversification.
* **Result:** A mathematically optimal allocation between high-growth (NVDA) and high-stability (TSMC) assets.

## 📊 Key Results

### Fundamental Ranking
The model identified **Value & Momentum** opportunities, highlighting companies like **Micron (MU)** and **SMIC (0981.HK)** as statistically attractive relative to their peers.

![Ranking Chart](output/quant_ranking_chart.png)

### Efficient Frontier Allocation
The optimization algorithm suggested a diversified mix, reducing portfolio volatility compared to a single-stock holding.

![Allocation Chart](output/portfolio_allocation.png)

## 🚀 How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Add LSEG App Key in `src/fetch_data.py`.
3. Run the pipeline:
   ```bash
   python src/fetch_data.py       # Get Data
   python src/analysis_model.py   # Rank Stocks
   python src/advanced_portfolio.py # Optimize Portfolio
