import json
import os


def load_entities():
    print("CURRENT WD: " + os.getcwd())
    entities = json.load(open(f"../registry/data/entities.json"))
    return entities


def get_entities():
    entities = load_entities()
    return entities


def get_entity(entity_slug):
    entities = load_entities()
    entity = [entity for entity in entities if entity["slug"] == entity_slug][0]
    return entity
