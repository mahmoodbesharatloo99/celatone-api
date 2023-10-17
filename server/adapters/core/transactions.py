from flask import abort
import logging
import requests

from utils.constants import WLD_URL
from utils.gcs import get_network_data
from utils.graphql import get_lcd_tx_responses, get_lcd_tx_results


def get_lcd_transaction(chain, network, tx_hash):
    return requests.get(f"{get_network_data(chain,network,'lcd')}/cosmos/tx/v1beta1/txs/{tx_hash}")


def get_wld_transaction(tx_hash):
    return requests.get(f"{WLD_URL}/txs/{tx_hash}")


def get_tx(chain, network, tx_hash):
    try:
        print("lcd_tx_results")
        graphql_res = get_lcd_tx_results(chain, network, tx_hash)
        graphql_tx_res = graphql_res["lcd_tx_results"]
        if graphql_tx_res:
            return graphql_tx_res[0]["result"]
    except Exception as e:
        logging.error(f"Error getting lcd_tx_results: {e}")
    try:
        print("lcd_tx_responses")
        graphql_res = get_lcd_tx_responses(chain, network, tx_hash, 1)
        graphql_tx_res = graphql_res["lcd_tx_responses"]
        if graphql_tx_res:
            return graphql_tx_res[0]["result"]
    except Exception as e:
        logging.error(f"Error getting lcd_tx_responses: {e}")
    try:
        print("lcd")
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
