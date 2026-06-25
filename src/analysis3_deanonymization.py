from address_to_wallet_mapping import get_wallet, load_cache, load_driver
import csv
from itertools import islice
import uuid
from collections import Counter

def read_first_k_chains(filepath: str, k: int) -> list[list[str]]:
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(islice(csv.reader(f), k))


cache = load_cache()
driver = load_driver()

bitcoin_address_chains = read_first_k_chains("../data/processed/simple_bet_chain_nodes.csv", 10)

wallet_address_chains = [[get_wallet(cache, driver, bitcoin_address) for bitcoin_address in chain] for chain in bitcoin_address_chains]

def summarize_chain(bitcoin_addresses: list[str], wallet_addresses: list[str]) -> dict:

    dominant_wallet_address, dominant_wallet_count = Counter(wallet_addresses).most_common(1)[0]

    return {
        "id": uuid.uuid4(),
        "chain_length": len(bitcoin_addresses),
        "unique_addresses": len(set(bitcoin_addresses)),
        "unique_wallets": len(set(wallet_addresses)),
        "dominant_wallet": dominant_wallet_address,
        "dominant_wallet_percentage": dominant_wallet_count / len(wallet_addresses) * 100,
    }

parsed = [summarize_chain(bitcoin_addresses, wallet_addresses)
          for bitcoin_addresses, wallet_addresses in zip(bitcoin_address_chains, wallet_address_chains)]

# TODO: Display results
print(parsed)