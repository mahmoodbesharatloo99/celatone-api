import os
from apiflask import APIFlask
from flask_cors import CORS
from entity.routes import blueprint as entity
from chain.routes import blueprint as chain
from images.routes import blueprint as images
from icns.routes import blueprint as icns
from core.osmosis.routes import blueprint as osmosis
from core.neutron.routes import blueprint as neutron
from core.sei.routes import blueprint as sei

app = APIFlask(__name__, title="My API", version="1.0")
CORS(app)

app.config["SYNC_LOCAL_SPEC"] = True
app.config["LOCAL_SPEC_PATH"] = os.path.join(app.root_path, "openapi.json")

## Utils ##
app.register_blueprint(entity)
app.register_blueprint(chain)
app.register_blueprint(images)
app.register_blueprint(icns)

## Chains ##
app.register_blueprint(osmosis)
app.register_blueprint(neutron)
app.register_blueprint(sei)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
