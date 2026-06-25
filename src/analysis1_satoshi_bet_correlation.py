from data_loader import read_parquet
from plots import plot_bet_correlation
from plot_map import plot_map

transactions = read_parquet("transactions")
satoshi_bets = transactions[transactions["is_satoshi_bet"]]

satoshi_bets = satoshi_bets.drop_duplicates(subset=["transaction_id", "output_position"])

def identity(x):
    return x

plot_map(
    amount_popular_dices=3,
    bets_dataframe=satoshi_bets,
    map_function=identity,
    plot_function=plot_bet_correlation
)