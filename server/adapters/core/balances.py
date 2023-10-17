from utils.gcs import get_network_data
import utils.helper as helper

LCD = "lcd"


def get_balances(chain, network, account_address):
    print(chain)
    try:
        native_balances = helper.get_native_balances(
            f"{get_network_data(chain, network, LCD)}",
            chain,
            network,
            account_address,
        )

        if chain == "terra":
            hive_balance = helper.get_hive_balance(chain, network, account_address)
            return native_balances + hive_balance

        return native_balances

    except Exception as e:
        # Handle or log the exception as needed
        print(f"Error getting balances: {e}")
        return None
