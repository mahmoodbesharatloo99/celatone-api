from flask import abort, Response
import requests
from utils.gcs import get_network_data


def get_rest(chain, network, path, params):
    try:
        response = requests.get(f"{get_network_data(chain,network,'lcd')}/{path}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as _:
        abort(Response(response=response.content, status=response.status_code, headers=response.headers.items()))


def get_graphql(chain, network, data):
    try:
        response = requests.post(get_network_data(chain, network, "graphql"), json=data)
        response.raise_for_status()
        return response.json()
    except:
        abort(Response(response=response.content, status=response.status_code, headers=response.headers.items()))
