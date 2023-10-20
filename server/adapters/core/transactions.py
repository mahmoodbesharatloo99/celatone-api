import logging
import requests
from flask import abort
from utils.graphql import get_lcd_tx_responses, get_lcd_tx_results
from utils.gcs import get_lcd_tx_results_from_gcs
from constants import LCD_DICT, WLD_URL


def get_lcd_transaction(chain, network, tx_hash):
    return requests.get(f"{LCD_DICT[chain][network]}/cosmos/tx/v1beta1/txs/{tx_hash}")


def get_wld_transaction(tx_hash):
    return requests.get(f"{WLD_URL}/txs/{tx_hash}")


def get_tx(chain, network, tx_hash):
    try:
        if (network == "osmosis-1"):
            gcp_res = get_lcd_tx_results_from_gcs(network, tx_hash)
            if gcp_res:
                logging.info(f"Got lcd_tx_results from GCS: {tx_hash}")
                return gcp_res
    except Exception as e:
        logging.error(f"Error getting lcd_tx_results: {e}")
    try:
        graphql_res = get_lcd_tx_results(chain, network, tx_hash)
        graphql_res.raise_for_status()
        graphql_tx_res = graphql_res.json()["data"]["lcd_tx_results"]
        if graphql_tx_res:
            return graphql_tx_res[0]["result"]
    except Exception as e:
        logging.error(f"Error getting lcd_tx_results: {e}")
    try:
        graphql_res = get_lcd_tx_responses(chain, network, tx_hash, 1)
        graphql_res.raise_for_status()
        graphql_tx_res = graphql_res.json()["data"]["lcd_tx_responses"]
        if graphql_tx_res:
            return graphql_tx_res[0]["result"]
    except Exception as e:
        logging.error(f"Error getting lcd_tx_responses: {e}")
    try:
        lcd = get_lcd_transaction(chain, network, tx_hash)
        lcd.raise_for_status()
        return lcd.json()
    except Exception as e:
        logging.error(f"Error getting lcd transaction: {e}")
    if chain == "sei" and network == "pacific-1":
        try:
            wld = get_wld_transaction(tx_hash)
            wld.raise_for_status()
            return wld.json()
        except Exception as e:
            logging.error(f"Error getting wld transaction: {e}")
    return abort(404)
