from utils.aldus import get_aldus_entities_data


def get_entities():
    entities = get_aldus_entities_data()
    return entities


def get_entity(entity_slug):
    entities = get_entities()
    entity = next(
        (entity for entity in entities if entity["slug"] == entity_slug), None
    )
    return entity
