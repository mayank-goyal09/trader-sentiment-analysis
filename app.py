import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Trader Sentiment Dashboard", layout="wide")

st.title("Bitcoin Trader Sentiment Analysis Dashboard")
st.markdown("Explore how hyperliquid traders alter their behaviors (leverage proxy, position sizing, frequency) based on general market fear/greed levels.")

# Cache the data loading so it's snappy
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sentiment = pd.read_csv(os.path.join(base_dir, 'data', 'fear_greed_index.csv'))
    trades = pd.read_csv(os.path.join(base_dir, 'data', 'historical_data.csv'))
    
    sentiment['date'] = pd.to_datetime(sentiment['date']).dt.date
    trades['Timestamp IST'] = pd.to_datetime(trades['Timestamp IST'], format='%d-%m-%Y %H:%M', errors='coerce')
    trades['date'] = trades['Timestamp IST'].dt.date
    trades.columns = [c.lower().replace(' ', '_') for c in trades.columns]
    trades = trades.dropna(subset=['date'])
    trades['is_win'] = trades['closed_pnl'] > 0
    trades['is_long'] = trades['direction'].str.lower().str.contains('buy', na=False) | trades['direction'].str.lower().str.contains('long', na=False)

    daily_trader = trades.groupby(['date', 'account']).agg(
        daily_pnl=('closed_pnl', 'sum'),
        trade_count=('account', 'count'),
        win_count=('is_win', 'sum'),
        avg_position_size=('size_usd', 'mean'),
        long_trades=('is_long', 'sum')
    ).reset_index()

    daily_trader['win_rate'] = daily_trader['win_count'] / daily_trader['trade_count']
    daily_trader['short_trades'] = daily_trader['trade_count'] - daily_trader['long_trades']
    daily_trader['ls_ratio'] = daily_trader['long_trades'] / (daily_trader['short_trades'] + 1)
    daily_trader['is_loss_day'] = daily_trader['daily_pnl'] < 0
    daily_trader['drawdown_proxy'] = np.where(daily_trader['daily_pnl'] < 0, daily_trader['daily_pnl'].abs(), 0)

    trader_sentiment = pd.merge(daily_trader, sentiment[['date', 'value', 'classification']], on='date', how='inner')

    def map_sentiment(c):
        if 'Fear' in c: return 'Fear'
        if 'Greed' in c: return 'Greed'
        return 'Neutral'

    trader_sentiment['sentiment_group'] = trader_sentiment['classification'].apply(map_sentiment)
    trades_analysis = trader_sentiment[trader_sentiment['sentiment_group'] != 'Neutral']

    trader_totals = trades_analysis.groupby('account')['trade_count'].sum().reset_index()
    med_freq = trader_totals['trade_count'].median()
    segment_map = dict(zip(trader_totals['account'], np.where(trader_totals['trade_count'] >= med_freq, 'Frequent', 'Infrequent')))
    trades_analysis['segment'] = trades_analysis['account'].map(segment_map)
    
    return trades_analysis

import numpy as np
data = load_data()

st.sidebar.header("Filter Data")
segment_filter = st.sidebar.multiselect("Select Trader Segment", options=data['segment'].unique(), default=data['segment'].unique())

filtered_data = data[data['segment'].isin(segment_filter)]

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Daily PnL by Sentiment")
    fig1, ax1 = plt.subplots(figsize=(5,4))
    sns.barplot(data=filtered_data, x="sentiment_group", y="daily_pnl", ax=ax1, palette="pastel")
    ax1.set_ylabel("Avg Daily PnL")
    st.pyplot(fig1)

with col2:
    st.subheader("Win Rate by Sentiment")
    fig2, ax2 = plt.subplots(figsize=(5,4))
    sns.barplot(data=filtered_data, x="sentiment_group", y="win_rate", ax=ax2, palette="deep")
    ax2.set_ylabel("Win Rate")
    st.pyplot(fig2)

with col3:
    st.subheader("Drawdown Proxy (Avg Loss)")
    fig3, ax3 = plt.subplots(figsize=(5,4))
    sns.barplot(data=filtered_data, x="sentiment_group", y="drawdown_proxy", ax=ax3, palette="muted")
    ax3.set_ylabel("Negative PnL Magnitude")
    st.pyplot(fig3)

st.markdown("---")

col4, col5 = st.columns(2)
with col4:
    st.subheader("Long/Short Ratio Bias")
    st.markdown("Are traders longing or shorting more heavily based on Fear/Greed?")
    fig4, ax4 = plt.subplots(figsize=(6,4))
    sns.boxplot(data=filtered_data, x="sentiment_group", y="ls_ratio", showfliers=False, ax=ax4, palette="Set2")
    st.pyplot(fig4)

with col5:
    st.subheader("Trade Frequency")
    st.markdown("Do users trade more often when they are greedy?")
    fig5, ax5 = plt.subplots(figsize=(6,4))
    sns.boxplot(data=filtered_data, x="sentiment_group", y="trade_count", showfliers=False, ax=ax5, palette="Set3")
    st.pyplot(fig5)
