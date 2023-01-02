import json


def load_accounts(chain, network):
    accounts = json.load(open(f"registry/data/{chain}/{network}/accounts.json"))
    return accounts


def get_accounts(chain, network):
    accounts = load_accounts(chain, network)
    return accounts


def get_account(chain, network, account_address):
    accounts = load_accounts(chain, network)
    account = [
        account for account in accounts if account["address"] == account_address
    ][0]
    return account
