from analysis3_address_to_wallet_mapping import get_wallet, load_cache, load_driver
import csv
from itertools import islice

def read_first_k_chains(filepath: str, k: int) -> list[list[str]]:
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(islice(csv.reader(f), k))


cache = load_cache()
driver = load_driver()

chains = read_first_k_chains("../data/processed/simple_bet_chain_nodes.csv", 10)

wallet_chains = [[get_wallet(cache, driver, bitcoin_address) for bitcoin_address in chain] for chain in chains]

print(wallet_chains)