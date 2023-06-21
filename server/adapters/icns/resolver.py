import requests
import base64

from constants import LCD_DICT

ICNS_RESOLVER_ADDRESS = (
    "osmo1xk0s8xgktn9x5vwcgtjdxqzadg88fgn33p8u9cnpdxwemvxscvast52cdd"
)


def get_icns_address(chain, network, name, bech32_prefix):
    QUERY_MSG = '{"address": {"name": "%s", "bech32_prefix": "%s"}}' % (
        name,
        bech32_prefix,
    )
    query_b64encoded = base64.b64encode(str.encode(QUERY_MSG)).decode("ascii")
    res = requests.get(
        f"{LCD_DICT['osmosis']['osmosis-1']}/cosmwasm/wasm/v1/contract/{ICNS_RESOLVER_ADDRESS}/smart/{query_b64encoded}"
    ).json()
    return res["data"]


def get_icns_names(chain, network, address):
    QUERY_MSG = '{"icns_names": {"address": "%s"}}' % (address,)
    query_b64encoded = base64.b64encode(str.encode(QUERY_MSG)).decode("ascii")
    res = requests.get(
        f"{LCD_DICT['osmosis']['osmosis-1']}/cosmwasm/wasm/v1/contract/{ICNS_RESOLVER_ADDRESS}/smart/{query_b64encoded}"
    ).json()
    return res["data"]
