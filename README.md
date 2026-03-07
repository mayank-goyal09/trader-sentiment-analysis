# Trader Sentiment Analysis

This project looks into how simple market emotion impacts actual trader behavior on Hyperliquid. By pulling together a Bitcoin Fear & Greed index alongside historical trade data, we can figure out if people really trade differently depending on the overall market mood.

## The Data We Used
- **fear_greed_index.csv**: Tells us if the market was feeling greedy, fearful, or neutral for a given day.
- **historical_data.csv**: A giant list of real trades with info like timestamps, trade size, direction (buy/sell), and PnL.

## How to Run It
All code and analysis is packaged nicely in `notebooks/analysis.ipynb`.  
1. `pip install -r requirements.txt`
2. Run `jupyter notebook notebooks/analysis.ipynb` and step through the cells to see the code execution and output generation.

---

## What We Found (Insights)

After engineering features like proxy drawdowns, long/short biases, and daily win rates, several patterns emerged:

1. **Greed drives larger drawdowns and bigger position sizing.**  
   *Evidence:* Looking at `position_size_vs_sentiment.png` and `drawdown_sentiment.png`, average position dollar sizing swells when things look optimistic. And consequently, when trades go against the user during Greed days, the average negative impact (drawdown proxy) is significantly worse.
   *Interpretation:* People get FOMO (Fear Of Missing Out). Because they see prices going up, they place larger bets thinking it's easy money.

2. **Frequent traders maintain their edge, infrequent traders bleed.**  
   *Evidence:* By segmenting accounts into "Frequent" and "Infrequent" groups, we see that frequent traders maintain much more stable behavior across different sentiment modes. Infrequent traders take much larger proportionate losses (drawdowns) during Extreme Greed compared to their baseline.
   *Interpretation:* Experienced traders probably have solid systems and position sizing limits. Casual traders abandon discipline when sentiment is high.

3. **Fear breeds aggressive short squeezing context.**  
   *Evidence:* The `ls_ratio_sentiment.png` metric reveals the average Long/Short ratio spikes upwards during Fear periods. 
   *Interpretation:* Counterintuitively, as the market hits "Fear", many traders start actively trying to catch the bottom by longing, which can create volatile localized setups.

---

## Strategy Ideas

Based on the data, here are two actionable rules you could apply:

### Rule 1: The Greed Size Cap
* **Market Condition:** Sentiment hits "Extreme Greed" or high "Greed".
* **Recommended Action:** Hard cap your position sizes by 20-30% and tighten stop-losses.
* **Expected Benefit:** Since our data shows casual traders size up way too heavily during these periods and take massive negative PnL outliers when wrong, forcing smaller bet sizes artificially protects capital from sudden reversals.

### Rule 2: Fade the "Fear" Bottom Fishers
* **Market Condition:** Market is deep in "Fear".
* **Recommended Action:** Since the Long/Short ratio data shows traders actually increase their relative longs trying to "catch the knife" during fear days, you can bet against the retail herd by utilizing short-biased setups until the L/S ratio neutralizes.
* **Expected Benefit:** Capitalize on the trapped liquidity of retail traders trying to call the bottom prematurely.

---

## Bonus Section
* **Predictive ML:** We successfully trained a Random Forest Classifier using daily sentiment, L/S bias, and frequency data. It achieved an ~71% accuracy when predicting whether the *following day* would net profitable returns for the cohort.
* **Streamlit App:** A lightweight dashboard was coded into `app.py` for direct interactive slicing of the charts by trader frequency segmentation. Run it with `streamlit run app.py`.
