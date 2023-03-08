import requests
from func.constants import LCD_DICT

def get_lcd_transaction(chain, network, tx_hash):
    return requests.get(f"{LCD_DICT[chain][network]}/cosmos/tx/v1beta1/txs/{tx_hash}")