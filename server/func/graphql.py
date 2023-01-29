import requests
from func.constants import GRAPHQL_DICT


def get_contract_instantiator_admin(chain, network, contract_addresses):
    contract_data = []
    query = "query {"
    for contract_address in contract_addresses:
        query += f"""
        {contract_address}: contracts_by_pk(address: "{contract_address}") {{
          account {{
            address
          }}
          accountByInitBy {{
            address
          }}  
        }}
        """
    query += "}"
    graphql_response = requests.post(
        GRAPHQL_DICT[chain][network], json={"query": query}
    ).json()["data"]
    for contract_address, data in graphql_response.items():
        if data["account"] is None:
            data["account"] = {"address": ""}
        if data["accountByInitBy"] is None:
            data["accountByInitBy"] = {"address": ""}
        contract_data.append(
            {
                "address": contract_address,
                "instantiator": data["accountByInitBy"]["address"],
                "admin": data["account"]["address"],
            }
        )
    return contract_data


if __name__ == "__main__":
    print(
        get_contract_instantiator_admin(
            "terra",
            "pisco-1",
            [
                "terra1suhgf5svhu4usrurvxzlgn54ksxmn8gljarjtxqnapv8kjnp4nrs0k5j44",
                "terra1xr3rq8yvd7qplsw5yx90ftsr2zdhg4e9z60h5duusgxpv72hud3ss3je3c",
            ],
        )
    )
