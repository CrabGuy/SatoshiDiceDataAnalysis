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

simple_bets = simple_bets[["transaction_id_x", "transaction_id_y", "output_address_id_x", "output_address_id_y"]]

MOST_POPULAR_DICE_ID = 3524394
popular_simple_bets = simple_bets[simple_bets["output_address_id_x"] == MOST_POPULAR_DICE_ID]

G = networkx.from_pandas_edgelist(
    popular_simple_bets,
    source="transaction_id_x",
    target="transaction_id_y",
    edge_attr=["output_address_id_y"],
    create_using=networkx.DiGraph,
)

# TODO: fix this one-liner
components = [list(networkx.get_edge_attributes(G.subgraph(component), "output_address_id_y").values()) for component in networkx.weakly_connected_components(G)]
component_lengths = [len(c) for c in components]

print(components)

length_distribution = pandas.Series(component_lengths).value_counts().sort_index()

mappings = read_parquet("mappings")

id_to_hash_map = mappings.set_index("address_id")["address_hash"].to_dict()
# TODO: refactor this and the rest into its own file
def save_to_csv(file_path, components: list[set]):

    mapped_components = [
        {id_to_hash_map[address_id] for address_id in nodes_set}
        for nodes_set in components
    ]

    mapped_components.sort(key=len, reverse=True)

    with open(file_path, 'w') as f:
        for s in mapped_components:
            f.write(','.join(map(str, s)) + '\n')

# TODO: plot distribution
print(length_distribution)
save_to_csv('../data/processed/simple_bet_chain_nodes.csv', components)