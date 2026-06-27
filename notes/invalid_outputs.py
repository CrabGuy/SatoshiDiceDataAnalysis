from src.data_loading.data_loader import read_dataset

outputs = read_dataset("outputs.csv", ["transaction_id", "output_position", "output_address_id", "amount", "script_type"])

duplicated = outputs.duplicated(subset=["transaction_id", "output_position"], keep=False)

invalid_outputs = outputs[duplicated].sort_values("transaction_id")

print(invalid_outputs)