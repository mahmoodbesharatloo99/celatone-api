from flask import redirect
from apiflask import APIBlueprint
from adapters.aldus import entities, projects
from adapters.aldus.chains import ChainManager
from utils.constants import ALDUS_URL


registry_bp = APIBlueprint("registry", __name__)


@registry_bp.route("/entities", methods=["GET"])
def get_entities():
    return entities.get_entities()


@registry_bp.route("/entities/<entity_slug>", methods=["GET"])
def get_entity(entity_slug):
    return entities.get_entity(entity_slug)


@registry_bp.route("/projects/<chain>/<network>", methods=["GET"])
def get_projects(chain, network):
    return projects.get_projects(chain, network)


@registry_bp.route("/projects/<chain>/<network>/<project_id>", methods=["GET"])
def get_project(chain, network, project_id):
    return projects.get_project(chain, network, project_id)


@registry_bp.route("/chains", methods=["GET"])
def get_chains():
    return ChainManager().get_chains()


@registry_bp.route("/chains/<chain>", methods=["GET"])
def get_chain(chain):
    return ChainManager().get_chain(chain)


@registry_bp.route("/images/entities/<entity_slug>", methods=["GET"])
def get_entity_image(entity_slug):
    return redirect(f"{ALDUS_URL}/assets/entities/{entity_slug}.png")


@registry_bp.route("/images/assets/<asset_symbol>", methods=["GET"])
def get_asset_image(asset_symbol):
    return redirect(f"{ALDUS_URL}/assets/assets/{asset_symbol}.png")
