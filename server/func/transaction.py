from flask import abort
from func.graphql import get_graphql_transaction
from func.lcd import get_lcd_transaction


def get_tx(chain, network, tx_hash):
    # get data from graphql
    graphql_res = get_graphql_transaction(chain, network, tx_hash, 1)
    graphql_tx_res = graphql_res.json()["data"]["lcd_tx_responses"]
    if len(graphql_tx_res):
        return graphql_tx_res[0]["result"]

    # if no data from graphql, get data from lcd
    lcd_res = get_lcd_transaction(chain, network, tx_hash)
    if lcd_res.status_code == 200:
        return lcd_res.json()

    return abort(404)
