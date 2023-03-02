import requests


def get_prices(chain, network, ids):
    prices = requests.get(
        f"https://celatone-price-cacher-h2bc4rnx5a-as.a.run.app/{chain}/{network}?ids={','.join(ids)}"
    ).json()
    return prices
