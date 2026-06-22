import pandas
from plots import plot_absolute_transaction_percentage, plot_relative_transaction_percentage
from data_loader import read_parquet

transactions = read_parquet("transactions", columns=["timestamp", "is_satoshi_bet", "amount", "transaction_id"])
satoshi_bets = transactions[transactions["is_satoshi_bet"]]

def resample(dataframe, start):
	TIME_STEP = "1ME"
	return dataframe[dataframe["timestamp"].between(start, "2023-12-31")].resample(TIME_STEP, on="timestamp")

sampled_transactions_amount = resample(transactions, satoshi_bets["timestamp"].min())["transaction_id"].nunique()
sampled_satoshi_bets = resample(satoshi_bets, satoshi_bets["timestamp"].min())["transaction_id"].nunique()

relative_amounts = (sampled_satoshi_bets / sampled_transactions_amount * 100)
print(relative_amounts)

plot_relative_transaction_percentage(relative_amounts)

absolute_amounts = pandas.DataFrame({
    "total": sampled_transactions_amount,
    "satoshi": sampled_satoshi_bets
})
print(absolute_amounts)

plot_absolute_transaction_percentage(absolute_amounts)