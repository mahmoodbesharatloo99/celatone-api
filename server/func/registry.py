import os
import json


def load_and_check_registry_data(chain, network, content):
    path = f"../registry/data/{chain}/{network}/{content}.json"
    data = []
    if os.path.exists(path):
        data = json.load(open(path))
    return data
