from src.data_loading.data_loader import read_parquet
from src.plotting.plots import plot_bet_correlation
from src.plotting.plot_map_popular import plot_map_popular

transactions = read_parquet("transactions")
satoshi_bets = transactions[transactions["is_satoshi_bet"]]

satoshi_bets = satoshi_bets.drop_duplicates(subset=["transaction_id", "output_position"])

def identity(x):
    return x

plot_map_popular(
    amount_popular_dices=3,
    bets_dataframe=satoshi_bets,
    map_function=identity,
    plot_function=plot_bet_correlation
)