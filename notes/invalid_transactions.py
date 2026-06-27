from src.data_loading.data_loader import read_dataset

transactions = read_dataset("transactions.csv", ["timestamp", "transaction_block_id", "transaction_id", "is_codebase", "transaction_fee"])

duplicated = transactions.duplicated(subset=["transaction_id"], keep=False)

invalid_transactions = transactions[duplicated].sort_values("transaction_id")

print(invalid_transactions)