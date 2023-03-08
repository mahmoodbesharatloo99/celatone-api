import json
from flask import abort
import requests
from func.graphql import get_graphql_transaction
from func.lcd import get_lcd_transaction

def get_tx(tx_hash):
    # get data from graphql
    graphql_res = get_graphql_transaction(tx_hash, 1)
    if (graphql_res.status_code == 200):
        return graphql_res.json()
    
    # if no data from graphql, get data from lcd
    lcd_res = get_lcd_transaction("osmosis", "osmo-test-4", tx_hash)
    if (lcd_res.status_code == 200):
        return lcd_res.json()
    
    return abort(404)
