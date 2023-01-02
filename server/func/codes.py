import requests


def get_codes(registry_url, chain, network):
    codes = requests.get(f"{registry_url}/data/{chain}/{network}/codes.json").json()
    return codes


def get_code(registry_url, chain, network, code_id):
    codes = requests.get(f"{registry_url}/data/{chain}/{network}/codes.json").json()
    code = [code for code in codes if code["id"] == code_id][0]
    return code
