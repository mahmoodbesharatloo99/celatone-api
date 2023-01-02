import json


def load_codes(chain, network):
    codes = json.load(open(f"registry/data/{chain}/{network}/codes.json"))
    return codes


def get_codes(chain, network):
    codes = load_codes(chain, network)
    return codes


def get_code(chain, network, code_id):
    codes = load_codes(chain, network)
    code = [code for code in codes if code["id"] == code_id][0]
    return code
