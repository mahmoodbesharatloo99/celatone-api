from flask import abort, Response
import requests
from constants import LCD_DICT


def get_rest(chain, network, path):
    try:
        response = requests.get(f"{LCD_DICT[chain][network]}/{path}")
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as _:
        abort(Response(response=response.content, status=response.status_code, headers=response.headers.items()))
