import func.constants as constants
import func.helper as helper


def get_balances(chain, network, account_address):
    if chain == "osmosis":
        return helper.get_native_balances(
            f"{constants.LCD_DICT[chain][network]}",
            chain,
            network,
            account_address,
        )
    elif chain == "terra":
        return helper.get_native_balances(
            f"{constants.LCD_DICT[chain][network]}",
            chain,
            network,
            account_address,
        ) + helper.get_hive_balance(chain, network, account_address)
    else:
        return []
