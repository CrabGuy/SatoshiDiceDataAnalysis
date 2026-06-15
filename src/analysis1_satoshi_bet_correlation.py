from data_loader import read_parquet

satoshi_bets = read_parquet("satoshi_bets")

# Probably no correlation, need to plot it
print(satoshi_bets["fee"].corr(satoshi_bets["amount"]))