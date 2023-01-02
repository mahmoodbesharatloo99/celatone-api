import requests


def get_accounts(registry_url, chain, network):
    accounts = requests.get(
        f"{registry_url}/data/{chain}/{network}/accounts.json"
    ).json()
    return accounts


def get_account(registry_url, chain, network, account_address):
    accounts = requests.get(
        f"{registry_url}/data/{chain}/{network}/accounts.json"
    ).json()
    account = [
        account for account in accounts if account["address"] == account_address
    ][0]
    return account
