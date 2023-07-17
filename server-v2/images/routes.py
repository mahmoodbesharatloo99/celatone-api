from apiflask import APIBlueprint
from .service import ImagesService

service = ImagesService()

blueprint = APIBlueprint("images", __name__, url_prefix="/images")

@blueprint.route("/entities/<entity_slug>", methods=["GET"])
def get_entity_image(entity_slug):
    return service.get_entity_image(entity_slug)


@blueprint.route("/assets/<asset_symbol>", methods=["GET"])
def get_asset_image(asset_symbol):
    return service.get_asset_image(asset_symbol)