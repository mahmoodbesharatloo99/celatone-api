import json


def load_entities():
    entities = json.load(open(f"../registry/data/entities.json"))
    return entities


def get_entities():
    entities = load_entities()
    return entities


def get_entity(entity_slug):
    entities = get_entities()
    entity = [entity for entity in entities if entity["slug"] == entity_slug][0]
    entity["logo_path"] = f"/images/entities/{entity_slug}"
    return entity
