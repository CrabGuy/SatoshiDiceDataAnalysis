import pandas
import networkx

from data_loader import read_parquet

transactions = read_parquet(
    "transactions",
    columns=["transaction_id", "output_position", "input_transaction_id", "input_transaction_position", "output_address_id", "is_satoshi_bet"]
)

grouped = transactions.groupby('transaction_id')

mask = (
    grouped['input_transaction_id'].transform('nunique') == 1
) & (
    grouped['output_position'].transform('nunique') == 2
) & (
    grouped['is_satoshi_bet'].transform("any")
)

simple_bets_transactions = transactions[mask]

# TODO: fix these names and make it more readable

simple_bets = pandas.merge(
    simple_bets_transactions,
    simple_bets_transactions,
    left_on=["input_transaction_id", "input_transaction_position"],
    right_on=["transaction_id", "output_position"]    
)

simple_bets = simple_bets[["transaction_id_x", "transaction_id_y", "output_address_id_x"]]

MOST_POPULAR_DICE_ID = 3524394
popular_simple_bets = simple_bets[simple_bets["output_address_id_x"] == MOST_POPULAR_DICE_ID]

G = networkx.from_pandas_edgelist(
    popular_simple_bets,
    source="transaction_id_x",
    target="transaction_id_y",
    edge_attr=["output_address_id_x"],
    create_using=networkx.DiGraph,
)

components = list(networkx.weakly_connected_components(G))
component_lengths = [len(c) for c in components]

length_distribution = pandas.Series(component_lengths).value_counts().sort_index()

# TODO: plot distribution
# TODO: save chains to a file
print(length_distribution)
print(components[0])