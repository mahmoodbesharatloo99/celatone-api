from abc import ABC, abstractmethod
from typing import List, Dict, Any
from utils.registry import load_and_check_registry_data
from utils.price import get_prices
from flask import abort, Response
from .graphql import get_lcd_tx_responses, get_lcd_tx_results
import requests
import logging
import constants

class BaseService(ABC):
    chain: str = None
    network: str = None

    def __init__(self):
        if self.chain is None or self.network is None:
            raise NotImplementedError("Subclasses must define `chain` and `network`.")
        
        self._accounts = load_and_check_registry_data(self.chain, self.network, "accounts")
        self._codes = load_and_check_registry_data(self.chain, self.network, "accounts")
        self._contracts = load_and_check_registry_data(self.chain, self.network, "contracts")
        self._assets = [
            dict(asset, **{"price": 0.00}) 
            for asset in load_and_check_registry_data(self.chain, self.network, "assets")
            ]
            
    @property
    def accounts(self) -> List[Dict]:
        return self._accounts

    @property
    def codes(self) -> Any:
        return self._codes

    @property
    def contracts(self) -> Any:
        return self._contracts
    
    @property
    def assets(self) -> Any:
        return self._assets

    def get_account(self, account_address: str) -> Dict:
        accounts = self.accounts()
        try:
            account = next(
                account for account in accounts if account["address"] == account_address
            )
        except StopIteration:
            raise ValueError(f"Account {account_address} not found")
        return account

    def get_assets_with_prices(self) -> List[Dict]:
        assets = self.assets()
        priced_assets = filter(lambda asset: asset["coingecko"], assets)
        priced_asset_ids = [asset["id"] for asset in priced_assets]
        prices = get_prices(self.chain, self.network, priced_asset_ids)
        asset_prices = {id: prices.get(id, 0.00) for id in priced_asset_ids}
        for asset in assets:
            asset["price"] = asset_prices.get(asset["id"], 0.00)
        return assets

    def get_assets_by_type(self, asset_type: str) -> List[Dict]:
        assets = self.assets()
        return list(filter(lambda asset: asset["type"] == asset_type, assets))

    def get_assets_by_slug(self, asset_slug: str) -> List[Dict]:
        assets = self.assets()
        return list(filter(lambda asset: asset_slug in asset["slugs"], assets))

    def get_asset(self, asset_id: int) -> Dict:
        assets = self.assets()
        asset_map = {asset["id"]: asset for asset in assets}
        return asset_map[asset_id]
    
    def get_asset_ibc(self, hash: str) -> List[Dict]:
        assets = self.assets()
        asset_map = {asset["id"]: asset for asset in assets}
        return asset_map[f"ibc/{hash}"]
    
    def get_balances(self, account_address):
        endpoint = f"{constants.LCD_DICT[self.chain][self.network]}"
        balances = (
        requests.get(
            f"{endpoint}/cosmos/bank/v1beta1/balances/{account_address}?pagination.limit=500"
            )
            .json()
            .get("balances", [])
        )
        supported_assets = self.get_assets_by_type("native")
        asset_ids = [asset["id"] for asset in supported_assets if asset["coingecko"] != ""]
        asset_prices = get_prices(asset_ids)
        output_balance = [
            {
                "name": asset["name"] if asset else None,
                "symbol": asset["symbol"] if asset else None,
                "id": balance["denom"],
                "amount": balance["amount"],
                "precision": asset["precision"] if asset else 0,
                "type": "native",
                "price": asset_prices.get(balance["denom"], 0)
                if asset and balance["denom"] in asset_prices
                else 0,
            }
            for balance in balances
            for asset in [
                next(
                    (
                        asset
                        for asset in supported_assets
                        if asset["id"] == balance["denom"]
                    ),
                    None,
                )
            ]
        ]
        return output_balance
    
    # TODO: Standardize Error Handling
    def get_rest(self, path: str):
        try:
            response = requests.get(f"{constants.LCD_DICT[self.chain][self.network]}/{path}")
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as _:
            abort(Response(response=response.content, status=response.status_code, headers=response.headers.items()))

    def get_tx(self, tx_hash: str):
        try:
            lcd = requests.get(f"{constants.LCD_DICT[self.chain][self.network]}/cosmos/tx/v1beta1/txs/{tx_hash}")
            lcd.raise_for_status()
            return lcd.json()
        except Exception as e:
            logging.error(f"Error getting lcd transaction: {e}")
        try:
            graphql_res = get_lcd_tx_results(self.chain, self.network, tx_hash)
            graphql_res.raise_for_status()
            graphql_tx_res = graphql_res.json()["data"]["lcd_tx_results"]
            if graphql_tx_res:
                return graphql_tx_res[0]["result"]
        except Exception as e:
            logging.error(f"Error getting lcd_tx_results: {e}")
        try:
            graphql_res = get_lcd_tx_responses(self.chain, self.network, tx_hash, 1)
            graphql_res.raise_for_status()
            graphql_tx_res = graphql_res.json()["data"]["lcd_tx_responses"]
            if graphql_tx_res:
                return graphql_tx_res[0]["result"]
        except Exception as e:
            logging.error(f"Error getting lcd_tx_responses: {e}")
        return abort(404)

