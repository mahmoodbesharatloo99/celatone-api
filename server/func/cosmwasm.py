

import json
import requests
import os
import base64

from func.constants import LCD_DICT
from func.registry import load_and_check_registry_data
from func.graphql import get_contract_instantiator_admin, get_graphql_code_details

# contracts

def get_contracts(chain, network):
    contracts = []
    contracts = load_and_check_registry_data(chain, network, "contracts")
    codes = load_and_check_registry_data(chain, network, "codes")
    if len(contracts) > 0:
        instantiator_admin_data = get_contract_instantiator_admin(
            chain, network, [contract["address"] for contract in contracts]
        )
        for contract in contracts:
            contract["description"] = ""
            contract["github"] = ""
            if "description" not in contract or contract["description"] == "":
                code_description = [code["description"] for code in codes if code["id"] == contract["code"]][0]
                contract["description"] = code_description
            if "github" not in contract or contract["github"] == "":
                code_github = [code["github"] for code in codes if code["id"] == contract["code"]][0]
                contract["github"] = code_github
            for data in instantiator_admin_data:
                if contract["address"] == data["address"]:
                    contract["instantiator"] = data["instantiator"]
                    contract["admin"] = data["admin"]
                    contract["label"] = data["label"]
    return contracts


def get_contract(chain, network, contract_address):
    contracts = get_contracts(chain, network)
    contract = [contract for contract in contracts if contract["address"] == contract_address][0]
    return contract



# codes

def load_codes(chain, network):
    codes = []
    path = f"../registry/data/{chain}/{network}/codes.json"
    if os.path.exists(path):
        codes = json.load(open(path))
        if len(codes) > 0:
            graphql_details = get_graphql_code_details(chain, network, [code["id"] for code in codes])
            for code in codes:
                code_graphql_detail = [detail for detail in graphql_details if detail["code_id"] == code["id"]][0]
                code["cw2Contract"] = code_graphql_detail["cw2_contract"]
                code["cw2Version"] = code_graphql_detail["cw2_version"]
                code["uploader"] = code_graphql_detail["creator"]
                code["contracts"] = code_graphql_detail["contract_instantiated"]
                code["instantiatePermission"] = code_graphql_detail["access_config_permission"]
                code["permissionAddresses"] = code_graphql_detail["access_config_addresses"]
    return codes


def get_codes(chain, network):
    codes = load_codes(chain, network)
    return codes


def get_code(chain, network, code_id):
    codes = load_codes(chain, network)
    code = [item for item in codes if int(item["id"]) == int(code_id)][0]
    return code


# helper

def get_upload_access(chain,network):
    upload_access = {}
    try:        
      res = requests.get(f"{LCD_DICT[chain][network]}/cosmwasm/wasm/v1/codes/params").json()
      upload_access = res["params"]["code_upload_access"]
    except:
        res = requests.get(f"{LCD_DICT[chain][network]}/cosmos/params/v1beta1/params?subspace=wasm&key=uploadAccess").json()
        res_value = json.loads(res["param"]["value"].replace("\\",""))
        upload_access = {
            "address":"",
            "addresses": res_value["addresses"],
            "permission": res_value["permission"]
        }
    return upload_access