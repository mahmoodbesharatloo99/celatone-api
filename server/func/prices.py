import requests


def chunks(ids):
    n = 10
    for i in range(0, len(ids), n):
        yield ids[i : i + n]


def get_prices(chain, network, ids):
    prices = {}
    id_chunks = chunks(ids)
    for id_chunk in id_chunks:
        prices.update(
            requests.get(
                f"https://celatone-price-cacher-h2bc4rnx5a-as.a.run.app/{chain}/{network}?ids={','.join(id_chunk)}"
            ).json()
        )
    return prices
