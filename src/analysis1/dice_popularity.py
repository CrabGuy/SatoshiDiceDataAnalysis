from src.plotting.plots import plot_satoshi_dice_popularity
from src.data_loading.data_loader import read_parquet
from src.data_loading.satoshi_dices_info import name, address_hash

transactions = read_parquet("transactions", columns=["is_satoshi_bet", "amount", "transaction_id", "output_address_id", "output_position"])
satoshi_bets = transactions[transactions["is_satoshi_bet"]]

satoshi_outputs = satoshi_bets.drop_duplicates(subset=["transaction_id", "output_address_id", "output_position"])[["output_address_id", "amount"]]

satoshi_bets_amount = satoshi_outputs.groupby(["output_address_id"]).agg(
    amount=("amount", "sum"),
    count=("amount", "count")
).reset_index()

satoshi_bets_amount["name"] = satoshi_bets_amount["output_address_id"].apply(address_hash).apply(name)

(   
    satoshi_bets_amount
    .sort_values(by="amount", ascending=False)["output_address_id"]
    .to_csv("./data/processed/sorted_satoshi_dices.csv", index=False, header=False)
)

plot_satoshi_dice_popularity(satoshi_bets_amount)