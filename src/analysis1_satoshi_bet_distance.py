import pandas
from data_loader import read_parquet
from plots import plot_bet_distance

transactions = read_parquet("transactions")
satoshi_bets = transactions[transactions["is_satoshi_bet"]]

def bet_distance(dataframe: pandas.DataFrame):
    dataframe = dataframe.drop_duplicates(subset="transaction_id")
    plot_bet_distance(dataframe.sort_values("transaction_block_id")["timestamp"].diff().dt.total_seconds())

# TODO: Do this also for the other 2 most popular
MOST_POPULAR_DICE_ID = 3524394
bet_distance(satoshi_bets[satoshi_bets["output_address_id"] == MOST_POPULAR_DICE_ID])