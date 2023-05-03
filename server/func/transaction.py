from flask import abort
from func.graphql import get_lcd_tx_responses, get_lcd_tx_results
from func.lcd import get_lcd_transaction


def get_tx(chain, network, tx_hash):
    # get data from graphql
    try:
        graphql_res = get_lcd_tx_results(chain, network, tx_hash)
        graphql_tx_res = graphql_res.json()["data"]["lcd_tx_results"]
        if len(graphql_tx_res):
            return graphql_tx_res[0]["result"]
    except:
        print("Graphql error")

    graphql_res = get_lcd_tx_responses(chain, network, tx_hash, 1)
    graphql_tx_res = graphql_res.json()["data"]["lcd_tx_responses"]
    if len(graphql_tx_res):
        return graphql_tx_res[0]["result"]
    return abort(404)
