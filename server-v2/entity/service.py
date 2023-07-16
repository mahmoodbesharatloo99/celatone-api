import json

class EntityService():
    
    def __init__(self):
        with open("../registry/data/entities.json") as f:
            self._entities = json.load(f)

    @property
    def entities(self):
        return self._entities
    
    def get_entity(self, entity_slug):
        entities = self.entities
        entity = next(
            (entity for entity in entities if entity["slug"] == entity_slug), None
        )
        if entity:
            entity["logo_path"] = f"/images/entities/{entity_slug}"
        return entity
    