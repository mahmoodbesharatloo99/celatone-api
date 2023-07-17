from utils.registry import load_and_check_registry_data
from core.base.base_service import BaseService
from flask import send_file

class ImagesService(BaseService):
    def get_entity_image(self, entity_slug):
        return send_file(f"../registry/assets/entities/{entity_slug}.png")
    
    def get_asset_image(self, asset_symbol):
        return send_file(f"../registry/assets/assets/{asset_symbol}.png")