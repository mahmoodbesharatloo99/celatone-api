from google.cloud import storage
import json

storage_client = storage.Client()

def get_lcd_tx_results_from_gcs(network, tx_hash):
    bucket = storage_client.bucket(network + "-lcd-tx-responses")
    blobs = bucket.list_blobs(prefix=tx_hash+"/", delimiter="/")
    # sort blobs by name desc after turn to int
    sorted_blobs = sorted(blobs, key=lambda blob: int(blob.name.split("/")[1]), reverse=True)
    if (len(sorted_blobs) == 0):
        return None
    res = sorted_blobs[0].download_as_string()
    return json.loads(res)
    