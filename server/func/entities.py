import json


def load_entities():
    with open("../registry/data/entities.json") as f:
        entities = json.load(f)
    return entities


def get_entities():
    entities = load_entities()
    return entities


def get_entity(entity_slug):
    entities = get_entities()
    entity = next((entity for entity in entities if entity["slug"] == entity_slug), None)
    if entity:
        entity["logo_path"] = f"/images/entities/{entity_slug}"
    return entity
