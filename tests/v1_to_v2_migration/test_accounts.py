import pytest
import requests
from .constant import *

@pytest.mark.parametrize("chain, network", [(chain, network) for chain in CHAINS for network in NETWORKS[chain]])
def test_get_accounts(chain, network):
    old_response = requests.get(f"{BASE_URL_OLD}/accounts/{chain}/{network}")
    new_response = requests.get(f"{BASE_URL_NEW}/{chain}/{network}/accounts")
    assert old_response.status_code == new_response.status_code
    assert old_response.json() == new_response.json(), f"The responses on {chain} {network} do not match"

@pytest.mark.parametrize("chain, network, address", 
                         [
                             ("osmosis", "osmosis-1", "osmo1pq47vuhc9gum8qjht0tamsgluuqjleqprgemhd")
                         ])
def test_get_account_valid_address(chain, network, address):
    old_response = requests.get(f"{BASE_URL_OLD}/accounts/{chain}/{network}/{address}")
    new_response = requests.get(f"{BASE_URL_NEW}/{chain}/{network}/accounts/{address}")
    assert old_response.status_code == new_response.status_code
    assert old_response.json() == new_response.json(), f"The responses on {chain} {network} do not match"

## TODO: Re-enable after finalize error standard with P'Tan
# @pytest.mark.parametrize("chain, network", [(chain, network) for chain in CHAINS for network in NETWORKS[chain]])
# def test_get_account_valid_address(chain, network):
#     INVALID_ADDRESS = "BLAHH"
#     old_response = requests.get(f"{BASE_URL_OLD}/accounts/{chain}/{network}/{INVALID_ADDRESS}")
#     new_response = requests.get(f"{BASE_URL_NEW}/{chain}/{network}/account/{INVALID_ADDRESS}")
#     assert old_response.status_code == new_response.status_code
#     assert old_response.json() == new_response.json(), f"The responses on {chain} {network} do not match"