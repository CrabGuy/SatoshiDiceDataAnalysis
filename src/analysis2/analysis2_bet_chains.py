import pandas
import networkx
from src.data_loading.satoshi_dices_info import k_most_popular_dices
from src.plotting.plots import plot_chain_length_distribution
from src.data_loading.data_loader import read_parquet
from src.analysis2.analysis2_bet_chains_functions import simple_bets, transaction_connections, edges_attribute, save_to_csv

transactions = read_parquet(
    "transactions",
    columns=["transaction_id", "output_position", "input_transaction_id", "input_transaction_position", "output_address_id", "is_satoshi_bet"]
)

simple_bet_transactions = simple_bets(transactions)

simple_bet_connections = transaction_connections(simple_bet_transactions)

most_popular_dice_id = k_most_popular_dices(1)[0]
popular_simple_bets_connections = simple_bet_connections[simple_bet_connections["input_address"] == most_popular_dice_id]

G = networkx.from_pandas_edgelist(
    popular_simple_bets_connections,
    source="input_id",
    target="output_id",
    edge_attr=["output_address"],
    create_using=networkx.DiGraph,
)

paths_nodes = [edges_attribute(G, component, "output_address") for component in networkx.weakly_connected_components(G)]
paths_lengths = [len(nodes) for nodes in paths_nodes]

length_distribution = pandas.Series(paths_lengths).value_counts().sort_index()

plot_chain_length_distribution(length_distribution)
save_to_csv('./data/processed/simple_bet_chain_nodes.csv', paths_nodes)