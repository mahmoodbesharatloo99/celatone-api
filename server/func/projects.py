import requests


def get_projects(registry_url, chain, network):
    projects = requests.get(
        f"{registry_url}/data/{chain}/{network}/projects.json"
    ).json()
    return projects


def get_project(registry_url, chain, network, project_id):
    projects = requests.get(
        f"{registry_url}/data/{chain}/{network}/projects.json"
    ).json()
    project = [project for project in projects if project["slug"] == project_id][0]
    return project
