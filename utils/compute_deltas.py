import pandas as pd
import os

def compute_balance_deltas(df):
    history_file = "data/history.csv"
    if os.path.exists(history_file):
        history_df = pd.read_csv(history_file)
        df = df.merge(history_df, on="Address", how="left", suffixes=("", "_prev"))
        df['Delta (BTC)'] = df['Balance (BTC)'] - df['Balance (BTC)_prev']
    else:
        df['Delta (BTC)'] = 0
    df[['Address', 'Balance (BTC)']].to_csv(history_file, index=False)
    return df

