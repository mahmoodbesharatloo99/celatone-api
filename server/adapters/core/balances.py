from utils.constants import LCD_DICT
import utils.helper as helper


def get_balances(chain, network, account_address):
    if chain == "terra":
        return helper.get_native_balances(
            f"{LCD_DICT[chain][network]}",
            chain,
            network,
            account_address,
        ) + helper.get_hive_balance(chain, network, account_address)
    else:
        return helper.get_native_balances(
            f"{LCD_DICT[chain][network]}",
            chain,
            network,
            account_address,
        )
