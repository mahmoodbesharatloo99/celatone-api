from adapters.registry.registry import load_and_check_registry_data


def get_accounts(chain, network):
    accounts = load_and_check_registry_data(chain, network, "accounts")
    return accounts


def get_account(chain, network, account_address):
    accounts = get_accounts(chain, network)
    try:
        account = next(
            account for account in accounts if account["address"] == account_address
        )
    except StopIteration:
        raise ValueError(f"Account {account_address} not found")
    return account
