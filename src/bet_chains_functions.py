import pandas
from satoshi_dices_info import address_hash

def simple_bets(transactions):
    grouped_transactions = transactions.groupby('transaction_id')

    simple_bet_mask = (
        grouped_transactions['input_transaction_id'].transform('nunique') == 1
    ) & (
        grouped_transactions['output_position'].transform('nunique') == 2
    ) & (
        grouped_transactions['is_satoshi_bet'].transform("any")
    )

    return transactions[simple_bet_mask]

def transaction_connections(transactions):
    connected = pandas.merge(
        transactions,
        transactions,
        left_on=["input_transaction_id", "input_transaction_position"],
        right_on=["transaction_id", "output_position"]    
    )

    connected = connected[["transaction_id_x", "output_address_id_x", "transaction_id_y", "output_address_id_y"]]
    connected.columns = ["input_id", "input_address", "output_id", "output_address"]

    return connected

def edges_attribute(graph, component, attribute):
    return [edge_data[attribute] for _, _, edge_data in graph.edges(component, data=True)]

def save_to_csv(file_path, components: list[set]):

    mapped_components = [
        {address_hash(address_id) for address_id in nodes_set}
        for nodes_set in components
    ]

    mapped_components.sort(key=len, reverse=True)

    def csv_format(address_set):
        return ','.join(map(str, address_set)) + '\n'

    with open(file_path, 'w') as f:
        for address_set in mapped_components:
            f.write(csv_format(address_set))