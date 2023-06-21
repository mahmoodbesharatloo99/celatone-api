import requests
import base64
import json
from urllib.parse import urljoin

from constants import LCD_DICT

ICNS_RESOLVER_ADDRESS = (
    "osmo1xk0s8xgktn9x5vwcgtjdxqzadg88fgn33p8u9cnpdxwemvxscvast52cdd"
)


def get_icns_address(name, bech32_prefix):
    query_msg = {"address": {"name": name, "bech32_prefix": bech32_prefix}}
    query_b64encoded = base64.b64encode(json.dumps(query_msg).encode("ascii")).decode(
        "ascii"
    )
    url = urljoin(
        LCD_DICT["osmosis"]["osmosis-1"],
        f"/cosmwasm/wasm/v1/contract/{ICNS_RESOLVER_ADDRESS}/smart/{query_b64encoded}",
    )
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()["data"]
    return data if data else {"address": ""}


def get_icns_names(address):
    query_msg = {"icns_names": {"address": address}}
    query_b64encoded = base64.b64encode(json.dumps(query_msg).encode("ascii")).decode(
        "ascii"
    )
    url = urljoin(
        LCD_DICT["osmosis"]["osmosis-1"],
        f"/cosmwasm/wasm/v1/contract/{ICNS_RESOLVER_ADDRESS}/smart/{query_b64encoded}",
    )
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()["data"]
    return data if data else {"names": [], "primary_name": None}
