import pandas
from plots import plot_absolute_transaction_percentage, plot_relative_transaction_percentage
from data_loader import read_parquet

transactions = read_parquet("transactions", columns=["timestamp", "is_satoshi_bet", "amount", "transaction_id"])
satoshi_bets = transactions[transactions["is_satoshi_bet"]]

earliest_satoshi_bet_timestamp = satoshi_bets["timestamp"].min()

def resample(dataframe, start, time_step="1ME"):
	return dataframe[dataframe["timestamp"].between(start, "2023-12-31")].resample(time_step, on="timestamp")

def resampled_amount(dataframe, start):
	return resample(dataframe, start)["transaction_id"].nunique()

transactions_amount = resampled_amount(transactions, earliest_satoshi_bet_timestamp)
satoshi_bets_amount = resampled_amount(satoshi_bets, earliest_satoshi_bet_timestamp)

relative_amounts = (satoshi_bets_amount / transactions_amount * 100)
print(relative_amounts)

plot_relative_transaction_percentage(relative_amounts)

absolute_amounts = pandas.DataFrame({
    "total": transactions_amount,
    "satoshi": satoshi_bets_amount
})
print(absolute_amounts)

plot_absolute_transaction_percentage(absolute_amounts)