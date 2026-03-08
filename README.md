# Trader Behavior vs Market Sentiment Analysis

## Overview

This project analyzes how **market sentiment (Fear vs Greed)** influences trader behavior and performance on Hyperliquid.
By combining a **Bitcoin Fear & Greed sentiment index** with **historical trading data**, the analysis explores whether traders adjust risk, trade frequency, or positioning based on overall market mood.

The objective is to identify **behavioral patterns** that can inform practical trading strategies.

---

## Datasets

### 1. Bitcoin Market Sentiment

**File:** `fear_greed_index.csv`
**Columns:**

* `date`
* `classification` (Fear / Greed)

This dataset provides the daily market sentiment classification.

### 2. Historical Trader Data

**File:** `historical_data.csv`

Key fields include:

* `account`
* `symbol`
* `execution_price`
* `size`
* `side`
* `time`
* `leverage`
* `closedPnL`
* `event`
* `start_position`

This dataset contains individual trade executions for Hyperliquid traders.

---

## Project Structure

```
trader-sentiment-analysis/
│
├ data/
│   ├ fear_greed_index.csv
│   └ historical_data.csv
│
├ notebooks/
│   └ analysis.ipynb
│
├ outputs/
│   ├ charts/
│   └ tables/
│
├ app.py
├ requirements.txt
└ README.md
```

---

## Methodology

### 1. Data Preparation

* Loaded both datasets using pandas
* Checked dataset dimensions, missing values, and duplicates
* Converted timestamps to datetime format
* Extracted **daily date values** from trading timestamps
* Aligned sentiment data with trading activity at the **daily level**

### 2. Data Merge

The two datasets were merged using the `date` column so that each trade is associated with the corresponding **market sentiment classification**.

### 3. Feature Engineering

Several behavioral and performance metrics were created:

**Performance Metrics**

* Daily PnL per trader
* Average PnL
* Win rate

**Behavioral Metrics**

* Trade frequency
* Average position size
* Leverage distribution
* Long vs Short ratio

**Risk Proxy**

* Negative PnL outliers used as a proxy for drawdowns

### 4. Trader Segmentation

To analyze behavioral differences, traders were grouped into segments:

* **Frequent traders vs Infrequent traders**
* **High leverage vs Low leverage traders**
* **Consistent vs Inconsistent performers**

Each segment was analyzed across different sentiment conditions.

---

## Key Insights

### 1. Position sizes increase during Greed periods

Average position sizing and leverage both increase when the market sentiment shifts to Greed.
This indicates higher risk appetite during optimistic market phases.

### 2. Infrequent traders experience larger losses during Greed

Traders with lower activity levels show significantly larger negative PnL outliers during Greed periods compared to frequent traders.

This suggests less disciplined risk management.

### 3. Long bias increases during Fear periods

The long/short ratio increases during Fear periods, indicating traders attempting to capture potential market reversals.

This behavior often occurs when participants try to “buy the dip”.

---

## Strategy Recommendations

### Strategy 1 — Position Size Control During Greed

**Condition:** Market sentiment classified as Greed
**Action:** Reduce maximum position sizing by ~20–30%

**Rationale:**
Larger positions during optimistic sentiment correlate with higher drawdown risk.

---

### Strategy 2 — Avoid Aggressive Bottom Fishing During Fear

**Condition:** Market sentiment classified as Fear

**Action:**
Avoid aggressive long entries until positioning normalizes.

**Rationale:**
The data shows increased long bias during Fear periods, suggesting traders often attempt premature market bottoms.

---

## Bonus Analysis

### Predictive Model

A **Random Forest classifier** was trained using sentiment and behavioral features such as:

* leverage
* trade frequency
* position size
* long/short bias

The model achieved approximately **71% accuracy** when predicting whether the next trading day would produce positive cohort-level profitability.
This model is exploratory and intended as a proof of concept.

---

### Interactive Dashboard

A lightweight **Streamlit dashboard** is included (`app.py`) to explore results interactively.

The dashboard allows users to:

* filter by sentiment regime
* analyze trader segments
* visualize PnL distributions

Run the dashboard with:

```
streamlit run app.py
```

---

## How to Run the Project

1. Clone the repository

```
git clone <repo-url>
cd trader-sentiment-analysis
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Run the notebook

```
jupyter notebook notebooks/analysis.ipynb
```

4. (Optional) Launch the dashboard

```
streamlit run app.py
```

---

## Conclusion

The analysis suggests that **market sentiment significantly influences trader behavior**, particularly in terms of position sizing and leverage usage.

Periods of Greed correspond to increased risk-taking, while Fear periods trigger stronger long positioning as traders attempt to capture reversals.

These behavioral patterns can be incorporated into **risk management rules or systematic trading strategies**.
