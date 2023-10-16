import json
import logging
from google.cloud import storage
from typing import Any, Dict


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
        data = get_gcs_data("celatone-endpoints", f"{endpoint}.json")
        return data[chain][network]
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
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        data = blob.download_as_text()  # Download blob as a string
        return json.loads(data)  # Parse JSON data
    except Exception as e:
        logging.error(f"Failed to get data from GCS: {e}")
        return {}
