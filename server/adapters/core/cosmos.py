from flask import abort, Response
import requests

from utils.constants import LCD_DICT, GRAPHQL_DICT


def get_rest(chain, network, path, params):
    try:
        response = requests.get(f"{LCD_DICT[chain][network]}/{path}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as _:
        abort(Response(response=response.content, status=response.status_code, headers=response.headers.items()))


def get_graphql(chain, network, data):
    try:
        response = requests.post(GRAPHQL_DICT[chain][network], json=data)
        response.raise_for_status()
        return response.json()
    except:
        abort(Response(response=response.content, status=response.status_code, headers=response.headers.items()))
