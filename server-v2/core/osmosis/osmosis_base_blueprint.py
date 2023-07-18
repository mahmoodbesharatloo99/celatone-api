from core.base.base_blueprint import BaseBlueprint
class OsmosisBaseBlueprint(BaseBlueprint):
    def __init__(self, service, name, url_prefix):
        super().__init__(service, name, url_prefix)

        ## Osmosis - Pools ##
        @self.blueprint.route("/pools", methods=["GET"])
        def get_pools():
            """Get All Pools

            Returns a list of all the known Osmosis pools based on the input chain and network
            """
            return self.service.pools

        @self.blueprint.route("/pool/<pool_id>", methods=["GET"])
        def get_pool(pool_id):
            """Get Pool by ID

            Returns a specific Osmosis pool based on the input chain, network, and code_id
            """
            return self.service.get_pool(pool_id)