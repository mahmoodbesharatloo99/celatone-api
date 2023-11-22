import requests
from utils.constants import PRICE_CACHER_URL


def chunks(ids):
    n = 10
    for i in range(0, len(ids), n):
        yield ids[i : i + n]


def get_prices(chain, network, ids):
    prices = {}
    id_chunks = chunks(ids)
    for id_chunk in id_chunks:
        res = requests.get(
            f"{PRICE_CACHER_URL}/{chain}/{network}?ids={','.join(id_chunk)}"
        ).json()
        prices.update({k: float(v) for (k, v) in res.items()})
    return prices
