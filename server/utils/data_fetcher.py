import requests
from utils.gcs import get_network_data


def fetch_paginated_data(
    url: str,
    data_key: str,
    sort_key: str = None,
):
    result = []
    pagination_key = None

    while True:
        if pagination_key:
            url += f"?pagination.key={pagination_key}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        result.extend(data[data_key])

        pagination_key = (
            data["pagination"].get("next_key") if "pagination" in data else None
        )
        if not pagination_key:
            break

    if sort_key:
        result = sorted(result, key=lambda x: x[sort_key])

    return {
        "items": result,
        "total": len(result),
    }
