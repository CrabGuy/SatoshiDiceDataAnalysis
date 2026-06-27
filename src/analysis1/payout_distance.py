from src.plotting.plots import plot_payout_distance_distribution
from src.data_loading.data_loader import read_parquet
import pandas

transactions = read_parquet("transactions", columns=["transaction_id", "transaction_block_id", "input_transaction_id", "is_satoshi_bet", "input_transaction_position", "output_position"])
# dropping transactions which don't have an input (which have not been spent yet)
transactions = transactions.dropna()

satoshi_payouts = pandas.merge(
    transactions[transactions["is_satoshi_bet"]],
    transactions,
    left_on=["input_transaction_id", "input_transaction_position"],
    right_on=["transaction_id", "output_position"]
)

block_delta = satoshi_payouts["transaction_block_id_x"] - satoshi_payouts["transaction_block_id_y"]

plot_payout_distance_distribution(block_delta)