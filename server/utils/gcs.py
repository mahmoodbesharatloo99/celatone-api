import json
import logging
from typing import Any, Dict

from google.cloud import storage

from .constants import ENDPOINT_BUCKET_NAME

storage_client = storage.Client()


def get_network_data(chain: str, network: str, endpoint: str) -> Dict[str, Any]:
    """
    Retrieves network data from a specified endpoint.

    Args:
        chain (str): The chain name.
        network (str): The network name.
        endpoint (str): The endpoint name.

    Returns:
        dict: The network data.
    """
    try:
        data = get_gcs_data(ENDPOINT_BUCKET_NAME, f"{endpoint}.json")
        if endpoint != "hive":
            return data[chain][network]
        else:
            return data[network]
    except Exception as e:
        logging.error(f"Failed to get network data: {e}")
        return {}


def get_gcs_data(bucket_name: str, source_blob_name: str) -> Dict[str, Any]:
    """
    Retrieves data from Google Cloud Storage.

    Args:
        bucket_name (str): The name of the bucket.
        source_blob_name (str): The name of the blob.

    Returns:
        dict: The data from the blob.
    """
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        data = blob.download_as_text()  # Download blob as a string
        return json.loads(data)  # Parse JSON data
    except Exception as e:
        logging.error(f"Failed to get data from GCS: {e}")
        return {}


def get_lcd_tx_response_from_gcs(network: str, tx_hash: str) -> Dict[str, Any]:
    """
    Retrieves LCD TX response from Google Cloud Storage.

    Args:
        network (str): Chain id.
        tx_hash (str): TX hash to query.

    Returns:
        dict: The data from the blob.
    """
    bucket = storage_client.bucket(network + "-lcd-tx-responses")
    blobs = bucket.list_blobs(prefix=tx_hash + "/", delimiter="/")
    # sort blobs by name desc after turn to int
    sorted_blobs = sorted(
        blobs, key=lambda blob: int(blob.name.split("/")[1]), reverse=True
    )
    if len(sorted_blobs) == 0:
        return {}
    res = sorted_blobs[0].download_as_string()
    return json.loads(res)
