from flask import Response, send_file

class ImagesService():
    def get_entity_image(self, entity_slug):
        try:
            response = send_file(f"../registry/assets/entities/{entity_slug}.png")
            if response.status_code == 200: return response
            else: raise FileNotFoundError()
        except:
            return Response(f"Entity Image {entity_slug} not found", status=404)
    
    def get_asset_image(self, asset_symbol):
        try:
            response = send_file(f"../registry/assets/assets/{asset_symbol}.png")
            if response.status_code == 200: return response
            else: raise FileNotFoundError()
        except:
            return Response(f"Asset Image {asset_symbol} not found", status=404)