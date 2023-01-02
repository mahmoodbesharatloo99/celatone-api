import requests


def get_entities(registry_url):
    entities = requests.get(f"{registry_url}/data/entities.json").json()
    return entities


def get_entity(registry_url, entity_slug):
    entities = requests.get(f"{registry_url}/data/entities.json").json()
    entity = [entity for entity in entities if entity["slug"] == entity_slug][0]
    return entity
