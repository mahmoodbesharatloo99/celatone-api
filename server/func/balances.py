import func.constants as constants
import func.helper as helper


def get_balances(chain, network, account_address):
    output_balances = []
    match chain:
        case "osmosis":
            output_balances = helper.get_native_balances(
                f"{constants.LCD_DICT[chain][network]}/cosmos/bank/v1beta1/balances",
                chain,
                network,
                account_address,
            )
        case "terra2":
            output_balances = helper.get_native_balances(
                f"{constants.LCD_DICT[chain][network]}/cosmos/bank/v1beta1/balances",
                chain,
                network,
                account_address,
            ) + helper.get_hive_balance(chain, network, account_address)
    return output_balances
