from src.data_loading.satoshi_dices_info import k_most_popular_dices

def filtered_bets(dataframe, address_id):
    return dataframe[dataframe["output_address_id"] == address_id]

def plot_map_popular(amount_popular_dices, bets_dataframe, map_function, plot_function):
    most_popular_dices = k_most_popular_dices(amount_popular_dices)

    distances = [map_function(filtered_bets(bets_dataframe, dice_id)) for dice_id in most_popular_dices]

    return plot_function([(distance, index + 1) for (index, distance) in enumerate(distances)])
