import requests
from func.constants import COINGECKO_API_KEY


""" def get_prices(assets):
    slugs = [asset["coingecko"] for asset in assets if asset["coingecko"] != None]
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(slugs)}&vs_currencies=usd&x_cg_pro_api_key={COINGECKO_API_KEY}"
    price_response = requests.get(url).json()
    for asset in assets:
        asset["price"] = 0
        if asset["coingecko"] != None:
            slug = asset["coingecko"]
            price_data = price_response[slug]
            price_usd = price_data["usd"]
            asset["price"] = price_usd
    return assets


def get_price(asset):
    slug = asset["coingecko"]
    asset["price"] = 0
    if slug is not None:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={slug}&vs_currencies=usd&x_cg_pro_api_key={COINGECKO_API_KEY}"
        price_response = requests.get(url).json()
        asset["price"] = price_response[slug]["usd"]
    return asset """

def get_prices(assets):
    return [1.00] * len(assets)

def get_price(asset):
    return 1.00

if __name__ == "__main__":
    get_prices(
        [
            {
                "name": "Osmosis",
                "symbol": "OSMO",
                "logo": "https://raw.githubusercontent.com/cosmos/chain-registry/master/osmosis/images/osmo.svg",
                "description": "The native token of Osmosis",
                "type": "native",
                "id": "uosmo",
                "precision": 6,
                "slugs": ["osmosis"],
                "coingecko": "osmosis",
                "coinmarketcap": "",
            }
        ]
    )
