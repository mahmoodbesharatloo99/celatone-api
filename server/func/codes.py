import json
import requests

from func.constants import SCANWORKS_URL


def load_codes(chain, network):
    codes = json.load(open(f"../registry/data/{chain}/{network}/codes.json"))
    verification_details = requests.get(
        f"{SCANWORKS_URL}/{chain}/contracts.json"
    ).json()["contracts"]
    for code in codes:
        if code["id"] in verification_details:
            code["verified"] = True
            code["verification_details"] = verification_details[code["id"]]
        else:
            code["verified"] = False
    return codes


def get_codes(chain, network):
    codes = load_codes(chain, network)
    return codes


def get_code(chain, network, code_id):
    codes = load_codes(chain, network)
    code = [code for code in codes if code["id"] == code_id][0]
    return code
