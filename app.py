import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from utils.fetch_data import get_top_wallets, get_wallet_balance

st.set_page_config(page_title="Bitcoin Whale Tracker — Top 100", layout="wide")
st.title("🐋 Bitcoin Whale Tracker Dashboard — Top 100")
st.markdown("Real-time monitoring of the top 100 Bitcoin wallets with change alerts.")

wallets = get_top_wallets()

# 🔹 Load previous history if exists
history_file = "data/history.json"
if os.path.exists(history_file):
    with open(history_file, "r") as f:
        history = json.load(f)
else:
    history = {}

data = []
alerts = []

THRESHOLD = 500  # threshold for change alert

for wallet in wallets:
    address = wallet["address"]
    balance = get_wallet_balance(address)
    prev_balance = history.get(address, None)
    
    # Check for change
    if prev_balance is not None:
        delta = balance - prev_balance
        if abs(delta) >= THRESHOLD:
            alerts.append({
                "address": address,
                "delta": delta,
                "balance": balance
            })
    
    # Save for display
    data.append({
        "Rank": wallet["rank"],
        "Address": address,
        "Balance (BTC)": balance
    })
    
    # Update history
    history[address] = balance

# Save history for next refresh
with open(history_file, "w") as f:
    json.dump(history, f)

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# 🔔 Display alerts based on changes
if alerts:
    st.markdown(f"### 🚨 Whale Movement Alert 🚨")
    for alert in alerts:
        direction = "increase" if alert["delta"] > 0 else "decrease"
        st.warning(f"Wallet {alert['address']} {direction} of {abs(alert['delta']):.2f} BTC (new balance: {alert['balance']:.2f} BTC)")
else:
    st.success("✅ No significant movements (±500 BTC) detected.")

st.caption(f"Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
