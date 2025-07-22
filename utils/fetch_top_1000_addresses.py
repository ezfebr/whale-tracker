import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_top_1000_wallets():
    url = "https://bitinfocharts.com/top-1000-richest-bitcoin-addresses.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    }

    print("🔎 Récupération des données en cours...")

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"⚠️ Erreur HTTP : {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    wallets = []

    # Sélecteur plus permissif : prend le premier tableau trouvé
    table = soup.find("table")
    if not table:
        print("⚠️ Tableau introuvable — vérifie la page source.")
        return

    rows = table.find_all("tr")[1:]

    for i, row in enumerate(rows[:1000]):
        cols = row.find_all("td")
        if len(cols) >= 2:
            address = cols[1].get_text(strip=True).replace("\n", "").replace(" ", "")
            wallets.append({
                "rank": i + 1,
                "address": address
            })

    # Crée dossier 'data' si manquant
    os.makedirs("data", exist_ok=True)

    # Sauvegarde
    with open("data/wallet_list.json", "w") as f:
        json.dump(wallets, f, indent=4)

    print(f"✅ {len(wallets)} adresses sauvegardées dans data/wallet_list.json.")

if __name__ == "__main__":
    fetch_top_1000_wallets()
