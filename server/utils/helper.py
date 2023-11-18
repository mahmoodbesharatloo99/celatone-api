import requests

from adapters.aldus.assets import AssetManager
from utils.gcs import get_network_data
import utils.prices as prices
import base64


def split(ls, n):
    return [ls[i : i + n] for i in range(0, len(ls), n)]


def generate_hive_query(account_address, contract_addresses):
    query = "query test {"
    for contract_address in contract_addresses:
        query += f"""
        {contract_address}: wasm{{
            contractQuery(contractAddress: "{contract_address}", query: {{
                balance: {{address : "{account_address}" }}
            }})
        }}
        """
    query += "}"
    return query


def get_hive_balance(chain, network, account_address):
    output_balance = []
    supported_assets = AssetManager(chain, network).get_assets_by_type("cw20")
    supported_assets_chunks = split(supported_assets, 50)
    asset_ids = [asset["id"] for asset in supported_assets if asset["coingecko"] != ""]
    asset_prices = prices.get_prices(chain, network, asset_ids)
    contract_addresses = [asset["id"] for asset in supported_assets]
    contract_address_chunks = split(contract_addresses, 50)
    for idx, contract_address_chunk in enumerate(contract_address_chunks):
        query = generate_hive_query(account_address, contract_address_chunk)
        print(get_network_data(chain, network, "hive"))
        hive_data = requests.post(
            f"{get_network_data(chain,network,'hive')}/graphql", json={"query": query}
        ).json()["data"]
        output_balance += [
            {
                "name": asset["name"],
                "symbol": asset["symbol"],
                "id": asset["id"],
                "amount": data.get("contractQuery", {}).get("balance", 0),
                "precision": asset["precision"],
                "type": "cw20",
                "price": asset_prices.get(asset["id"], 0)
                if asset and asset["id"] in asset_prices
                else 0,
            }
            for asset, data in zip(
                supported_assets_chunks[idx],
                [
                    hive_data.get(contract_address, {})
                    for contract_address in contract_address_chunk
                ],
            )
            if int(data.get("contractQuery", {}).get("balance", 0)) > 0
        ]
    return output_balance


def get_native_balances(endpoint, chain, network, account_address):
    balances = (
        requests.get(
            f"{endpoint}/cosmos/bank/v1beta1/balances/{account_address}?pagination.limit=500"
        )
        .json()
        .get("balances", [])
    )
    supported_assets = AssetManager(chain, network).get_assets_by_type("native")
    asset_ids = [asset["id"] for asset in supported_assets if asset["coingecko"] != ""]
    asset_prices = prices.get_prices(chain, network, asset_ids)
    output_balance = [
        {
            "name": asset["name"] if asset else None,
            "symbol": asset["symbol"] if asset else None,
            "id": balance["denom"],
            "amount": balance["amount"],
            "precision": asset["precision"] if asset else 0,
            "type": "native",
            "price": asset_prices.get(balance["denom"], 0)
            if asset and balance["denom"] in asset_prices
            else 0,
        }
        for balance in balances
        for asset in [
            next(
                (
                    asset
                    for asset in supported_assets
                    if asset["id"] == balance["denom"]
                ),
                None,
            )
        ]
    ]
    return output_balance


def get_cw20_balance(chain, network, account_address):
    # TODO: generalize to support multiple cw20 tokens using multicall
    contract_address = "sei1eavtmc4y00a0ed8l9c7l0m7leesv3yetcptklv2kalz4tsgz02mqlvyea6"
    query = f'{{"balance": {{"address": "{account_address}"}}}}'
    encoded_query = base64.b64encode(query.encode()).decode()
    print(encoded_query)
    res = requests.get(
        f"{get_network_data(chain, network, 'lcd')}/cosmwasm/wasm/v1/contract/{contract_address}/smart/{encoded_query}"
    ).json()
    return [
        {
            "amount": res["data"]["balance"],
            "id": "sei1eavtmc4y00a0ed8l9c7l0m7leesv3yetcptklv2kalz4tsgz02mqlvyea6",
            "name": "Poker Kings Token",
            "precision": 6,
            "price": 0,
            "symbol": "PKS",
            "type": "cw20",
        }
    ]
