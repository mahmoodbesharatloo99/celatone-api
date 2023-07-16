from apiflask import APIBlueprint
from .service import EntityService

service = EntityService()

blueprint = APIBlueprint("entity", __name__)

@blueprint.route("/entities", methods=["GET"])
def entities():
    return service.entities

@blueprint.route("/entity/<slug>", methods=["GET"])
def entityBySlug(slug: str) :
    return service.get_entity(slug)

