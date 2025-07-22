import json
import requests

def get_top_wallets():
    with open("data/wallet_list.json") as f:
        wallets = json.load(f)
    return wallets

def get_wallet_balance(address):
    url = f"https://blockstream.info/api/address/{address}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            funded = data["chain_stats"]["funded_txo_sum"]
            spent = data["chain_stats"]["spent_txo_sum"]
            balance = (funded - spent) / 1e8
            return balance
        else:
            return 0
    except Exception:
        return 0

