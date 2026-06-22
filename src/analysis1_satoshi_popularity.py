from plots import plot_satoshi_dice_popularity
from data_loader import read_parquet

transactions = read_parquet("transactions", columns=["is_satoshi_bet", "amount", "transaction_id", "output_address_id", "output_position"])
satoshi_bets = transactions[transactions["is_satoshi_bet"]]
satoshi_dices = read_parquet("satoshi_dices")

complete_transactions = satoshi_bets.merge(satoshi_dices, left_on="output_address_id", right_on="address_id").drop_duplicates(subset=["transaction_id", "output_address_id", "output_position"])
complete_transactions = complete_transactions.drop(columns=["output_address_id"])

satoshi_bets_amount = complete_transactions.groupby(["address_hash", "name"]).agg(
    amount=("amount", "sum"),
    count=("amount", "count")
).reset_index()

print(satoshi_bets_amount)

plot_satoshi_dice_popularity(satoshi_bets_amount)