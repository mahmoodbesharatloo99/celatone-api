from flask import Flask, send_file
import os
from apiflask import APIFlask
from flask_cors import CORS
from osmosis.osmosis_1.routes import osmosis_1_blueprint

app = APIFlask(__name__, title="My API", version="1.0")
CORS(app)

app.config["SYNC_LOCAL_SPEC"] = True
app.config["LOCAL_SPEC_PATH"] = os.path.join(app.root_path, "openapi.json")
app.config["TAGS"] = [
    {
        "name": "Default",
        "description": "Default queries",
    },
    {
        "name": "Registry Data",
        "description": "Queries that uses data from the registry data JSONs",
    },
    {
        "name": "Registry Assets",
        "description": "Queries that uses data from the registry data asset images",
    },
    {
        "name": "External",
        "description": "Queries that uses also uses data from external sources",
    },
]

app.register_blueprint(osmosis_1_blueprint, url_prefix='/osmosis/osmosis-1')

if __name__ == "__main__":
    app.run(debug=True)
