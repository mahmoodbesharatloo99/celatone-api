from abc import ABC
import json
from typing import List, Dict

from utils.registry import load_and_check_registry_data, load_projects, get_project, load_codes
from utils.price import get_prices
from flask import abort, Response
from utils.graphql import get_lcd_tx_responses, get_lcd_tx_results
import requests
import logging
import constants

class BaseService(ABC):
    chain: str = None
    network: str = None

    def __init__(self):
        if self.chain is None or self.network is None:
            raise NotImplementedError("Subclasses must define `chain` and `network`.")
        
        self._accounts = load_and_check_registry_data(
            chain=self.chain, 
            network=self.network, 
            content="accounts"
            )
        
        self._codes = load_codes(
            chain=self.chain, 
            network=self.network
            )
        
        self._contracts = load_and_check_registry_data(
            chain=self.chain, 
            network=self.network, 
            content="contracts"
            )
        
        self._assets = [
            dict(asset, **{"price": 0.00}) 
            for asset in load_and_check_registry_data(
                chain=self.chain, 
                network=self.network, 
                content="assets"
                )
            ]
        self._projects = load_projects(
            accounts=self._accounts, 
            assets=self._assets, 
            codes=self._codes, 
            contracts=self._contracts
            )
            
    @property
    def accounts(self) -> List[Dict]:
        return self._accounts

    @property
    def codes(self) -> List[Dict]:
        return self._codes

    @property
    def contracts(self) -> List[Dict]:
        return self._contracts
    
    @property
    def assets(self) -> List[Dict]:
        return self._assets
    
    @property
    def projects(self) -> List[Dict]:
        return self._projects

    def get_account(self, account_address: str) -> Dict:
        accounts = self.accounts
        try:
            account = next(
                account for account in accounts if account["address"] == account_address
            )
        except StopIteration:
            # Remark: Legacy Error Handling
            # raise ValueError(f"Account {account_address} not found")
            
            return Response((f"Account {account_address} not found"), status=404)
        return account

    def get_assets_with_prices(self) -> List[Dict]:
        assets = [asset.copy() for asset in self.assets]
        priced_assets = filter(lambda asset: asset["coingecko"], assets)
        priced_asset_ids = [asset["id"] for asset in priced_assets]
        prices = get_prices(self.chain, self.network, priced_asset_ids)
        asset_prices = {id: prices.get(id, 0.00) for id in priced_asset_ids}
        for asset in assets:
            asset["price"] = asset_prices.get(asset["id"], 0.00)
        return assets

    def get_assets_by_type(self, asset_type: str) -> List[Dict]:
        assets = self.assets
        return list(filter(lambda asset: asset["type"] == asset_type, assets))

    def get_assets_by_slug(self, asset_slug: str) -> List[Dict]:
        assets = self.assets
        return list(filter(lambda asset: asset_slug in asset["slugs"], assets))

    def get_asset(self, asset_id: int) -> Dict:
        assets = self.assets
        asset_map = {asset["id"]: asset for asset in assets}
        if asset_id in asset_map:
            return asset_map[asset_id]
        else:
            return Response("Asset Not found", status=404)
    
    def get_asset_ibc(self, hash: str) -> List[Dict]:
        assets = self.assets
        asset_map = {asset["id"]: asset for asset in assets}
        if f"ibc/{hash}" in asset_map:
            return asset_map[f"ibc/{hash}"]
        else:
            return Response("Asset Not found", status=404)
    
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
    
    # TODO: Use the `projects` injected in the service and manually filter them
    def get_project(self, slug: str):
        return get_project(self.accounts, self.assets, self.codes, self.contracts, slug)

    # TODO: Handle invalid code_id / list index out of range
    def get_code(self, code_id):
        codes = self.codes
        code = [code for code in codes if code["id"] == int(code_id)][0]
        return code
    
    def get_upload_access(self):
        upload_access = {}
        res = requests.get(f"{constants.LCD_DICT[self.chain][self.network]}/wasm/params")
        if res.status_code == 200:
            upload_access = res.json().get("params", {}).get("code_upload_access", {})
        else:
            res = requests.get(
                f"{constants.LCD_DICT[self.chain][self.chain][self.network]}/cosmos/params/v1beta1/params?subspace=wasm&key=uploadAccess"
            ).json()
            res_value = json.loads(res["param"]["value"])
            permission = res_value["permission"]
            addresses = res_value.get("addresses", [])
            address = addresses[0] if permission == "OnlyAddress" else ""
            upload_access = {
                "permission": permission,
                "addresses": addresses,
                "address": address,
            }
        return upload_access