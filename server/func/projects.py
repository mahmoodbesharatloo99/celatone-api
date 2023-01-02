import json


def load_projects(chain, network):
    projects = json.load(open(f"registry/data/{chain}/{network}/projects.json"))
    return projects


def get_projects(chain, network):
    projects = load_projects(chain, network)
    return projects


def get_project(chain, network, project_id):
    projects = load_projects(chain, network)
    project = [project for project in projects if project["slug"] == project_id][0]
    return project
