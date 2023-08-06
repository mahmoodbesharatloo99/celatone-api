from typing import Any, List, Dict

from flask import Response
from utils.registry import load_and_check_registry_data
from core.base.base_service import BaseService

class OsmosisBaseService(BaseService):
    def __init__(self):
        super().__init__()
        self._pools = load_and_check_registry_data(
            chain=self.chain,
            network=self.network, 
            content="pools"
        )

    @property
    def pools(self):
        return self._pools
    
    def get_pool(self, pool_id):
        pools = self.pools
        pool = next(filter(lambda pool: pool["id"] == int(pool_id), pools), None)
        return pool
    
    ## Remark: Not used yet
    def get_asset_factory(self, creator, symbol):
        assets = self.get_assets_with_prices()
        asset_map = {asset["id"]: asset for asset in assets}
        return asset_map[f"factory/{creator}/{symbol}"]

    ## Remark: Not used yet
    def get_asset_gamm(self, pool_id):
        assets = self.get_assets_with_prices()
        asset_map = {asset["id"]: asset for asset in assets}
        if f"gamm/pool/{pool_id}" in asset_map:
            return asset_map[f"gamm/pool/{pool_id}"]
        else: 
            return Response("Asset Gamm Not Found", status=404)
