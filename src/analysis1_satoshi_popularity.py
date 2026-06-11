import pandas
from plots import plot_satoshi_dice_popularity
satoshi_bets = pandas.read_parquet("../data/processed/satoshi_bets.parquet")

print(satoshi_bets.columns)

satoshi_bets_amount = satoshi_bets.groupby(["hash", "Name"]).agg(
    amount=("amount", "sum"),
    count=("amount", "count")
).reset_index()

plot_satoshi_dice_popularity(satoshi_bets_amount)