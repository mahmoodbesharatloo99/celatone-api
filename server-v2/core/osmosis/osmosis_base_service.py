from typing import Any, List, Dict
from core.base.base_service import BaseService

class OsmosisBaseService(BaseService):
    def get_asset_factory(self, creator, symbol):
        assets = self.get_assets_with_prices()
        asset_map = {asset["id"]: asset for asset in assets}
        return asset_map[f"factory/{creator}/{symbol}"]


    def get_asset_gamm(self, pool_id):
        assets = self.get_assets_with_prices()
        asset_map = {asset["id"]: asset for asset in assets}
        return asset_map[f"gamm/pool/{pool_id}"]
