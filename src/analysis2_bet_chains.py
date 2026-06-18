from data_loader import read_parquet

inputs = read_parquet("inputs")
outputs = read_parquet("outputs")
transactions = read_parquet("transactions")
mappings = read_parquet("mappings")

transactions = inputs[["previous_transaction_id", "transaction_id"]].merge(transactions[["transaction_id"]]).merge(outputs[["transaction_id", "address_id"]])
transactions = transactions.rename(columns={"previous_transaction_id": "input_id", "address_id": "output_id"})
