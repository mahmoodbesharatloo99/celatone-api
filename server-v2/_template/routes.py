from apiflask import APIBlueprint
from .service import TemplateService

service = TemplateService()

blueprint = APIBlueprint("blueprint_name", __name__, url_prefix="/some_prefix")

@blueprint.route("/endpoint_name", methods=["GET"])
def field():
    return service.field()