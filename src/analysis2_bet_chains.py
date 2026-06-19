import pandas
import networkx

from data_loader import read_parquet

def build_transaction_graph(df: pandas.DataFrame) -> networkx.DiGraph:
    G = networkx.DiGraph()
    G.add_nodes_from(df["transaction_id"])

    output_to_tx = dict(zip(df["change_id"], df["transaction_id"]))

    edges = (
        (output_to_tx[row.input_id], row.transaction_id)
        for row in df.itertuples()
        if row.input_id in output_to_tx
    )

    G.add_edges_from(edges)
    return G

def shortest_path_length_distribution(G: networkx.DiGraph) -> pandas.Series:
    lengths = dict(networkx.all_pairs_shortest_path_length(G))

    s = pandas.Series([
        l
        for source, targets in lengths.items()
        for target, l in targets.items()
        if l > 0
    ])

    return s.value_counts().sort_index()

inputs = read_parquet("inputs")
outputs = read_parquet("outputs")
transactions = read_parquet("transactions")
satoshi_dices = read_parquet("satoshi_dices")
mappings = read_parquet("mappings")

satoshi_dices = set(satoshi_dices.merge(mappings, left_on="Address", right_on="hash")["address_id"])

transactions = inputs[["previous_transaction_id", "transaction_id"]].merge(transactions[["transaction_id"]]).merge(outputs[["transaction_id", "address_id"]])
transactions = transactions.rename(columns={"previous_transaction_id": "input_id", "address_id": "output_id"})


transactions["is_dice_output"] = transactions["output_id"].isin(satoshi_dices)

grouped = transactions.groupby('transaction_id')

mask = (
    grouped['input_id'].transform('nunique') == 1
) & (
    grouped['output_id'].transform('nunique') == 2
) & (
    grouped['is_dice_output'].transform("any")
)

simple_bets_transactions = transactions[mask]

simple_bets = (
    simple_bets_transactions
    .sort_values("is_dice_output")
    .groupby("transaction_id").agg(
        input_id = ("input_id", "first"),
        change_id = ("output_id", "first"),
        dice_id = ("output_id", "last")
    )
    .reset_index()
)

MOST_POPULAR_DICE_ID = 3524394
popular_simple_bets = simple_bets[simple_bets["dice_id"] == MOST_POPULAR_DICE_ID]

G = build_transaction_graph(popular_simple_bets)

path_length_distribution = shortest_path_length_distribution(G)

# Plot this and fix up the rest of the plotting
print(path_length_distribution)