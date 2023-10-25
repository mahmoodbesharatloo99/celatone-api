from typing import Any, Dict
from flask import abort, Response
import requests
from utils.gcs import get_network_data


def handle_error(response: requests.Response) -> None:
    """Abort the request and return an error response."""
    abort(
        Response(
            response=response.content,
            status=response.status_code,
            headers=response.headers.items(),
        )
    )


def get_rest(
    chain: str, network: str, path: str, params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Send a GET request to the specified path and return the response.

    Parameters:
    chain (str): The blockchain chain.
    network (str): The network.
    path (str): The path to send the request to.
    params (dict): The parameters to include in the request.

    Returns:
    dict: The response from the request.
    """
    try:
        response = requests.get(
            f"{get_network_data(chain,network,'lcd')}/{path}", params=params
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError:
        handle_error(response)


def post_rest(
    chain: str, network: str, path: str, data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Perform a POST request to the specified path and return the response.

    Parameters:
    chain (str): The blockchain chain.
    network (str): The network.
    path (str): The path to send the request to.
    data (dict): The payload to be sent with the request

    Returns:
    dict: The response from the request.
    """
    try:
        response = requests.post(
            f"{get_network_data(chain, network, 'lcd')}/{path}", data=data
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError:
        handle_error(response)


def get_graphql(chain: str, network: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send a POST request to the specified path and return the response.

    Parameters:
    chain (str): The blockchain chain.
    network (str): The network.
    data (dict): The data to include in the request.

    Returns:
    dict: The response from the request.
    """
    try:
        response = requests.post(get_network_data(chain, network, "graphql"), json=data)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError:
        handle_error(response)
