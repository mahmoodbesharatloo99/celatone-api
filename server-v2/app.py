from flask import Flask, send_file
import os
from apiflask import APIFlask
from flask_cors import CORS
from core.osmosis.routes import blueprint as osmosis
from entity.routes import blueprint as entity
from chain.routes import blueprint as chain

app = APIFlask(__name__, title="My API", version="1.0")
CORS(app)

app.config["SYNC_LOCAL_SPEC"] = True
app.config["LOCAL_SPEC_PATH"] = os.path.join(app.root_path, "openapi.json")


app.register_blueprint(osmosis)
app.register_blueprint(entity)
app.register_blueprint(chain)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
