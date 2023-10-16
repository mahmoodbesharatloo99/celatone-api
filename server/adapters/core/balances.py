from utils.gcs import get_network_data
import utils.helper as helper


def get_balances(chain, network, account_address):
    if chain == "terra":
        return helper.get_native_balances(
            f"{get_network_data(chain,network,'lcd')}",
            chain,
            network,
            account_address,
        ) + helper.get_hive_balance(chain, network, account_address)
    else:
        return helper.get_native_balances(
            f"{get_network_data(chain,network,'lcd')}",
            chain,
            network,
            account_address,
        )
