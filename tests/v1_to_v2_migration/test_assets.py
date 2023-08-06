import pytest
import requests
from .constant import *

@pytest.mark.parametrize("chain, network", [(chain, network) for chain in CHAINS for network in NETWORKS[chain]])
def test_get_assets(chain, network):
    old_response = requests.get(f"{BASE_URL_OLD}/assets/{chain}/{network}")
    new_response = requests.get(f"{BASE_URL_NEW}/{chain}/{network}/assets")
    assert old_response.status_code == new_response.status_code
    assert old_response.json() == new_response.json(), f"The responses on {chain} {network} do not match"

@pytest.mark.parametrize("chain, network", [(chain, network) for chain in CHAINS for network in NETWORKS[chain]])
def test_get_assets_with_prices(chain, network):
    old_response = requests.get(f"{BASE_URL_OLD}/assets/{chain}/{network}/prices")
    new_response = requests.get(f"{BASE_URL_NEW}/{chain}/{network}/assets/prices")
    assert old_response.status_code == new_response.status_code
    assert old_response.json() == new_response.json(), f"The responses on {chain} {network} do not match"

@pytest.mark.parametrize("chain, network", [(chain, network) for chain in CHAINS for network in NETWORKS[chain]])
def test_get_assets_by_valid_type(chain, network):
    asset_type = "native"
    old_response = requests.get(f"{BASE_URL_OLD}/assets/{chain}/{network}/type/{asset_type}")
    new_response = requests.get(f"{BASE_URL_NEW}/{chain}/{network}/assets/type/{asset_type}")
    assert old_response.status_code == new_response.status_code
    assert old_response.json() == new_response.json(), f"The responses on {chain} {network} do not match"

@pytest.mark.parametrize("chain, network", [(chain, network) for chain in CHAINS for network in NETWORKS[chain]])
def test_get_assets_by_invalid_type(chain, network):
    asset_type = "FOO"
    old_response = requests.get(f"{BASE_URL_OLD}/assets/{chain}/{network}/type/{asset_type}")
    new_response = requests.get(f"{BASE_URL_NEW}/{chain}/{network}/assets/type/{asset_type}")
    assert old_response.status_code == new_response.status_code
    assert old_response.json() == new_response.json(), f"The responses on {chain} {network} do not match"

@pytest.mark.parametrize("chain, network", [(chain, network) for chain in CHAINS for network in NETWORKS[chain]])
def test_get_assets_by_valid_slug(chain, network):
    slug = "binance"
    old_response = requests.get(f"{BASE_URL_OLD}/assets/{chain}/{network}/slug/{slug}")
    new_response = requests.get(f"{BASE_URL_NEW}/{chain}/{network}/assets/slug/{slug}")
    assert old_response.status_code == new_response.status_code
    assert old_response.json() == new_response.json(), f"The responses on {chain} {network} do not match"

@pytest.mark.parametrize("chain, network", [(chain, network) for chain in CHAINS for network in NETWORKS[chain]])
def test_get_assets_by_invalid_slug(chain, network):
    slug = "FOO"
    old_response = requests.get(f"{BASE_URL_OLD}/assets/{chain}/{network}/slug/{slug}")
    new_response = requests.get(f"{BASE_URL_NEW}/{chain}/{network}/assets/slug/{slug}")
    assert old_response.status_code == new_response.status_code
    assert old_response.json() == new_response.json(), f"The responses on {chain} {network} do not match"

@pytest.mark.parametrize(
        "chain, network, hash", 
        [
            ## JUNO ##
            ("osmosis", "osmosis-1", "46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BED"),
            ("osmosis", "osmo-test-5", "8E2FEFCBD754FA3C97411F0126B9EC76191BAA1B3959CB73CECF396A4037BBF0"),
            ("stargaze", "stargaze-1", "448C1061CE97D86CC5E86374CD914870FB8EBA16C58661B5F1D3F46729A2422D"),

            ## USDC ##
            ("neutron", "neutron-1", "F082B65C88E4B6D5EF1DB243CDA1D331D002759E938A0F5CD3FFDC5D53B3E349"),
            ("osmosis", "osmo-test-5", "6F34E1BD664C36CE49ACC28E60D62559A5F96C4F9A6CCE4FC5A67B2852E24CFE")
        ])
def test_get_asset_ibc_valid_hash(chain, network, hash):
    old_response = requests.get(f"{BASE_URL_OLD}/assets/{chain}/{network}/ibc/{hash}")
    new_response = requests.get(f"{BASE_URL_NEW}/{chain}/{network}/assets/ibc/{hash}")
    assert old_response.status_code == new_response.status_code
    assert old_response.json() == new_response.json(), f"The responses on {chain} {network} do not match"

@pytest.mark.parametrize("chain, network", [(chain, network) for chain in CHAINS for network in NETWORKS[chain]])
def test_get_asset_ibc_invalid_hash(chain, network):
    INVALID_HASH = "46B44899322F3CD854D2D46DEEF881958467CDD4B3B10086DA49296BBED94BEA"
    old_response = requests.get(f"{BASE_URL_OLD}/assets/{chain}/{network}/ibc/{INVALID_HASH}")
    new_response = requests.get(f"{BASE_URL_NEW}/{chain}/{network}/assets/ibc/{INVALID_HASH}")
    assert old_response.status_code == 500
    assert new_response.status_code == 404

## TODO: Implement this one after get_asset_factory is used
def test_get_asset_factory():
    pass

## TODO: Re-enable this one after get_asset_gamm is used
# @pytest.mark.parametrize(
#         "network, pool_id", [
#             ("osmosis-1", "1"),
#             ("osmo-test-4", "2")
#         ])
# def test_get_asset_gamm_valid_id(network, pool_id):
#     old_response = requests.get(f"{BASE_URL_OLD}/assets/osmosis/{network}/gamm/pool/{pool_id}")
#     new_response = requests.get(f"{BASE_URL_NEW}/osmosis/{network}/assets/gamm/pool/{pool_id}")
#     assert old_response.status_code == new_response.status_code
#     assert old_response.json() == new_response.json(), f"The responses on {network} with Pool {pool_id} do not match"


@pytest.mark.parametrize("network", [(network) for network in NETWORKS["osmosis"]])
def test_get_asset_gamm_invalid_id(network):
    INVALID_POOL_ID = 100000
    old_response = requests.get(f"{BASE_URL_OLD}/assets/osmosis/{network}/gamm/pool/{INVALID_POOL_ID}")
    new_response = requests.get(f"{BASE_URL_NEW}/osmosis/{network}/assets/gamm/pool/{INVALID_POOL_ID}")
    assert old_response.status_code == 500
    assert new_response.status_code == 404



