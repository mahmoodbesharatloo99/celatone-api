import requests


def get_prices(ids):
    prices = requests.get(
        f"https://celatone-price-cacher-h2bc4rnx5a-as.a.run.app/prices?denoms={','.join(ids)}"
    ).json()
    return prices
