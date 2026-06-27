import pandas
from src.data_loading.data_loader import read_dataset, save_parquet

inputs = read_dataset("inputs.csv", ["transaction_id", "input_transaction_id", "input_transaction_position"])

outputs = read_dataset("outputs.csv", ["transaction_id", "output_position", "output_address_id", "amount", "script_type"])
outputs = outputs.drop(columns=["script_type"])
invalid_outputs = outputs.duplicated(subset=["transaction_id", "output_position"], keep=False)
outputs = outputs[~invalid_outputs]

transactions = read_dataset("transactions.csv", ["timestamp", "transaction_block_id", "transaction_id", "is_codebase", "transaction_fee"])
transactions = transactions.drop(columns=["is_codebase"])
invalid_transactions = transactions.duplicated(subset=["transaction_id"], keep=False)
transactions = transactions[~invalid_transactions]
transactions["timestamp"] = pandas.to_datetime(transactions["timestamp"], unit="s")

complete_transactions = transactions.merge(inputs, how="left").merge(outputs, how="left")

mappings = read_dataset("mappings.csv", ["address_hash", "address_id"])
save_parquet(mappings, "mappings")

satoshi_dices = pandas.read_csv("./data/raw/satoshiDiceInfos.tsv", sep='\t')[["Name", "Address"]]
satoshi_dices.columns = ["name", "address_hash"]
satoshi_dices = satoshi_dices.merge(mappings)

complete_transactions["is_satoshi_bet"] = complete_transactions["output_address_id"].isin(satoshi_dices["address_id"])

save_parquet(complete_transactions, "transactions")
save_parquet(satoshi_dices, "satoshi_dices")