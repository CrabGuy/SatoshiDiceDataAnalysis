from data_loader import read_parquet
from plots import plot_bet_correlation
import pandas

transactions = read_parquet("transactions")
satoshi_bets = transactions[transactions["is_satoshi_bet"]]

def bet_correlation(dataframe: pandas.DataFrame):
    dataframe = dataframe.drop_duplicates(subset="transaction_id")
    print(f'Correlation: {dataframe["transaction_fee"].corr(dataframe["amount"])}')
    plot_bet_correlation(dataframe, "transaction_fee", "amount")

# TODO: Do this also for the other 2 most popular
MOST_POPULAR_DICE_ID = 3524394
bet_correlation(satoshi_bets[satoshi_bets["output_address_id"] == MOST_POPULAR_DICE_ID])