from utils import balances
from utils.gcs import get_network_data


def get_balances_legacy(chain, network, account_address):
    print(chain)
    try:
        native_balances = balances.get_native_balances_legacy(
            f"{get_network_data(chain, network, 'lcd')}",
            chain,
            network,
            account_address,
        )

        if chain == "terra":
            hive_balance = balances.get_hive_balance_legacy(
                chain, network, account_address
            )
            return native_balances + hive_balance

        return native_balances

    except Exception as e:
        # Handle or log the exception as needed
        print(f"Error getting balances: {e}")
        return None


def get_balances(chain, network, address):
    native_balances = balances.get_native_balances(chain, network, address)
    if chain == "terra":
        hive_balance = balances.get_hive_balance(chain, network, address)
        native_balances.append(hive_balance)
    return native_balances
