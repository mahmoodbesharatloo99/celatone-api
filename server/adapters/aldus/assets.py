import base64

from utils.aldus import get_aldus_chain_data
from utils.prices import get_prices

from typing import List, Dict, Any, Optional


class AssetManager:
    def __init__(self, chain: str, network: str):
        """
        Initializes the AssetManager with assets data.

        Parameters:
        chain (str): The blockchain chain.
        network (str): The network.
        """
        self.chain = chain
        self.network = network
        self.assets = get_aldus_chain_data(chain, network, "assets")
        self.asset_map = {asset["id"]: asset for asset in self.assets}

    def get_assets(self) -> List[Dict[str, Any]]:
        """
        Fetches and sorts assets data.

        Returns:
        List[Dict[str, Any]]: A list of assets.
        """
        return sorted([dict(asset, **{"price": 0.00}) for asset in self.assets], key=lambda d: d["symbol"])

    def get_asset(self, asset_id: str) -> Dict[str, Any]:
        """
        Fetches a specific asset by its ID.

        Parameters:
        asset_id (str): The ID of the asset.

        Returns:
        Dict[str, Any]: The asset data.
        """
        try:
            return self.asset_map[asset_id]
        except KeyError:
            raise ValueError(f"No asset found with ID {asset_id}")

    def get_assets_by_type(self, asset_type: str) -> List[Dict[str, Any]]:
        """
        Fetches assets by their type.

        Parameters:
        asset_type (str): The type of the asset.

        Returns:
        List[Dict[str, Any]]: A list of assets.
        """
        return list(filter(lambda asset: asset["type"] == asset_type, self.assets))

    def get_assets_by_slug(self, asset_slug: str) -> List[Dict[str, Any]]:
        """
        Fetches assets by their slug.

        Parameters:
        asset_slug (str): The slug of the asset.

        Returns:
        List[Dict[str, Any]]: A list of assets.
        """
        return list(filter(lambda asset: asset_slug in asset["slugs"], self.assets))

    def get_asset_ibc(self, hash: str) -> Optional[Dict[str, Any]]:
        """
        Fetches a specific asset by its IBC hash.

        Parameters:
        hash (str): The IBC hash of the asset.

        Returns:
        Dict[str, Any]: The asset data.
        """
        try:
            return self.asset_map[f"ibc/{hash}"]
        except KeyError:
            return None

    def get_asset_factory(self, creator: str, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Fetches a specific asset by its creator and symbol.

        Parameters:
        creator (str): The creator of the asset.
        symbol (str): The symbol of the asset.

        Returns:
        Dict[str, Any]: The asset data.
        """
        try:
            return self.asset_map[f"factory/{creator}/{symbol}"]
        except KeyError:
            return None

    def get_asset_gamm(self, pool_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetches a specific asset by its pool ID.

        Parameters:
        pool_id (str): The pool ID of the asset.

        Returns:
        Dict[str, Any]: The asset data.
        """
        try:
            return self.asset_map[f"gamm/pool/{pool_id}"]
        except KeyError:
            return None

    def get_assets_with_prices(self) -> List[Dict[str, Any]]:
        """
        Fetches and sorts assets data with their prices.

        Returns:
        List[Dict[str, Any]]: A list of assets with their prices.
        """
        priced_assets = filter(lambda asset: asset["coingecko"], self.assets)
        priced_asset_ids = [asset["id"] for asset in priced_assets]
        prices = get_prices(self.chain, self.network, priced_asset_ids)
        asset_prices = {id: prices.get(id, 0.00) for id in priced_asset_ids}
        for asset in self.assets:
            asset["price"] = asset_prices.get(asset["id"], 0.00)
        return self.assets
