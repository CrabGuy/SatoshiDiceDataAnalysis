from plots import plot_satoshi_dice_popularity
from data_loader import read_parquet
satoshi_bets = read_parquet("satoshi_bets")

satoshi_bets_amount = satoshi_bets.groupby(["hash", "Name"]).agg(
    amount=("amount", "sum"),
    count=("amount", "count")
).reset_index()

plot_satoshi_dice_popularity(satoshi_bets_amount)