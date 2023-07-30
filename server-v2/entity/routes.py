from apiflask import APIBlueprint
from .service import EntityService

service = EntityService()

blueprint = APIBlueprint("entity", __name__, url_prefix="/entities")

@blueprint.route("", methods=["GET"])
def entities():
    return service.entities

@blueprint.route("/<slug>", methods=["GET"])
def entityBySlug(slug: str) :
    return service.get_entity(slug)

