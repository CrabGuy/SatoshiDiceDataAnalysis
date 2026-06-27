from src.data_loading.satoshi_dices_info import k_most_popular_dices, address_hash, name

popular_dices = [name(address_hash(dice)) for dice in k_most_popular_dices(3)]

print(popular_dices)