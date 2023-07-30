import pytest
import requests
from .constant import *

def test_get_chains():
    old_response = requests.get(f"{BASE_URL_OLD}/chains")
    new_response = requests.get(f"{BASE_URL_NEW}/chains")
    assert old_response.status_code == new_response.status_code
    assert old_response.json() == new_response.json(), f"The responses on do not match"

@pytest.mark.parametrize("chain", [
    "osmosis",
    "neutron"
])
def test_get_chain(chain):
    old_response = requests.get(f"{BASE_URL_OLD}/chains/{chain}")
    new_response = requests.get(f"{BASE_URL_NEW}/chains/{chain}")
    assert old_response.status_code == new_response.status_code
    assert old_response.json() == new_response.json(), f"The responses on {chain} do not match"

def test_get_chain_invalid_chain():
    INVALID_CHAIN = "BLAH"
    old_response = requests.get(f"{BASE_URL_OLD}/chains/{INVALID_CHAIN}")
    new_response = requests.get(f"{BASE_URL_NEW}/chains/{INVALID_CHAIN}")
    assert old_response.status_code == 500
    assert new_response.status_code == 404