import logging
from flask import abort
from func.graphql import get_lcd_tx_responses, get_lcd_tx_results
from func.lcd import get_lcd_transaction


def get_tx(chain, network, tx_hash):
    try:
        lcd = get_lcd_transaction(chain, network, tx_hash).json()
        return lcd
    except Exception as e:
        logging.error(f"Error getting lcd transaction: {e}")
    try:
        graphql_res = get_lcd_tx_results(chain, network, tx_hash)
        graphql_tx_res = graphql_res.json()["data"]["lcd_tx_results"]
        if graphql_tx_res:
            return graphql_tx_res[0]["result"]
    except Exception as e:
        logging.error(f"Error getting lcd_tx_results: {e}")
    try:
        graphql_res = get_lcd_tx_responses(chain, network, tx_hash, 1)
        graphql_tx_res = graphql_res.json()["data"]["lcd_tx_responses"]
        if graphql_tx_res:
            return graphql_tx_res[0]["result"]
    except Exception as e:
        logging.error(f"Error getting lcd_tx_responses: {e}")
    return abort(404)
