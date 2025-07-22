import json

def parse_clean_address_list(input_path="data/top100.txt", output_path="data/wallet_list.json"):
    wallets = []
    with open(input_path, "r") as f:
        for i, line in enumerate(f):
            address = line.strip()
            if address:
                wallets.append({
                    "rank": i + 1,
                    "address": address
                })

    with open(output_path, "w") as f:
        json.dump(wallets, f, indent=4)

    print(f"✅ {len(wallets)} adresses sauvegardées dans {output_path}")

if __name__ == "__main__":
    parse_clean_address_list()
