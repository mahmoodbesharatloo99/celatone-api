from apiflask import APIBlueprint

class BaseBlueprint:
    def __init__(self, service, name, url_prefix):
        self.service = service
        self.blueprint = APIBlueprint(name, __name__, url_prefix=url_prefix)

        ### ACCOUNT ###
        @self.blueprint.route("/accounts", methods=["GET"])
        def accounts():
            return self.service.accounts

        @self.blueprint.route("/account/<account_address>", methods=["GET"])
        def account(account_address: str):
            return self.service.get_account(account_address)

        ### ASSETS ###
        @self.blueprint.route("/assets", methods=["GET"])
        def get_assets():
            """Get All Assets

            Returns a list of all the known assets based on the input chain and network
            """
            return self.service.assets

        @self.blueprint.route('/assets/prices', methods=["GET"])
        def get_assets_prices():
            """Get All Assets with Prices

            Returns a list of all the known assets based on the input chain and network
            """
            return self.service.get_assets_with_prices()

        @self.blueprint.route('/assets/type/<asset_type>', methods=["GET"])
        def get_assets_by_type(asset_type):
            """Get Assets by Type

            Returns a list of all the known assets based on the input chain, network, and asset_type
            """
            return self.service.get_assets_by_type(asset_type)

        @self.blueprint.route('/assets/slug/<asset_slug>', methods=["GET"])
        def get_asset_by_slug(asset_slug):
            return self.service.get_assets_by_slug(asset_slug)

        @self.blueprint.route('/assets/<asset_id>', methods=["GET"])
        def get_asset(asset_id):
            return self.service.get_asset(asset_id)
        
        @self.blueprint.route('/assets/ibc/<hash>', methods=["GET"])
        def get_asset_ibc(hash):
            return self.service.get_asset_ibc(hash)

        ## Code ##
        @self.blueprint.route("/codes", methods=["GET"])
        def get_codes():
            return self.service.codes
        
        @self.blueprint.route("/code/<code_id>", methods=["GET"])
        def get_code(code_id):
            return self.service.get_code(code_id)

        ## Project ##
        @self.blueprint.route("/projects", methods=["GET"])
        def get_projects():
            return self.service.projects

        @self.blueprint.route("/projects/<slug>", methods=["GET"])
        def get_project(slug):
            return self.service.get_project(slug)

        ## Cosmos Rest ##
        @self.blueprint.route("/rest/<path:path>", methods=["GET"])
        def get_some_rest(path):
            return self.service.get_rest(path)
        
        @self.blueprint.route("/upload_access", methods=["GET"])
        def get_upload_access():
            """Get Upload Access

            Returns the upload access for the input chain and network
            """
            return service.get_upload_access()

    def get_blueprint(self):
        return self.blueprint
