import base64
import json
import requests
from urllib.parse import urljoin

from utils.gcs import get_network_data

ICNS_RESOLVER_ADDRESS = "osmo1xk0s8xgktn9x5vwcgtjdxqzadg88fgn33p8u9cnpdxwemvxscvast52cdd"
NETWORK_NAME = "osmosis"
NETWORK_VERSION = "osmosis-1"
LCD = "lcd"


def get_icns_data(query_msg):
    query_b64encoded = base64.b64encode(json.dumps(query_msg).encode("ascii")).decode("ascii")
    url = urljoin(
        get_network_data(NETWORK_NAME, NETWORK_VERSION, LCD),
        f"/cosmwasm/wasm/v1/contract/{ICNS_RESOLVER_ADDRESS}/smart/{query_b64encoded}",
    )
    res = requests.get(url)
    res.raise_for_status()
    data = res.json().get("data", {})
    return data


def get_icns_address(name, bech32_prefix):
    query_msg = {"address": {"name": name, "bech32_prefix": bech32_prefix}}
    data = get_icns_data(query_msg)
    return data if data else {"address": ""}


def get_icns_names(address):
    query_msg = {"icns_names": {"address": address}}
    data = get_icns_data(query_msg)
    return data if data else {"names": [], "primary_name": None}
