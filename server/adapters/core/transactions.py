import logging
import requests
from flask import abort
from utils.graphql import get_lcd_tx_responses, get_lcd_tx_results
from constants import LCD_DICT


def get_lcd_transaction(chain, network, tx_hash):
    return requests.get(f"{LCD_DICT[chain][network]}/cosmos/tx/v1beta1/txs/{tx_hash}")


def get_tx(chain, network, tx_hash):
    try:
        lcd = get_lcd_transaction(chain, network, tx_hash)
        lcd.raise_for_status()
        return lcd.json()
    except Exception as e:
        logging.error(f"Error getting lcd transaction: {e}")
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
    return abort(404)
