from data_loader import read_parquet
import pandas

most_popular_dices = pandas.read_csv("../data/processed/sorted_satoshi_dices.csv", header=None)[0]

def k_most_popular_dices(k):
    return most_popular_dices.head(k).to_list()

mappings = read_parquet("mappings")
satoshi_dices = read_parquet("satoshi_dices")

id_to_hash_map = mappings.set_index("address_id")["address_hash"].to_dict()

def address_hash(address_id):
    return id_to_hash_map[address_id]

def name(address_hash: str):
    return satoshi_dices[satoshi_dices["address_hash"] == address_hash]["name"].iloc[0]
