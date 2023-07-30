import pytest
import requests
from .constant import *

## In the old module, get_codes doesn't work on some chains, i.e., sei-atlantic-2
## check with P'Tan
# @pytest.mark.parametrize("chain, network", [(chain, network) for chain in CHAINS for network in NETWORKS[chain]])
# def test_get_codes(chain, network):
#     old_response = requests.get(f"{BASE_URL_OLD}/codes/{chain}/{network}")
#     new_response = requests.get(f"{BASE_URL_NEW}/{chain}/{network}/codes")
#     if (old_response.status_code == 200):
#         assert old_response.status_code == new_response.status_code
#         assert old_response.json() == new_response.json(), f"The responses on {chain} {network} do not match"
#     else:
#         assert new_response.status_code == 200
#         assert new_response.json() == []
