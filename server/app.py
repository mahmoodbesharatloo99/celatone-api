import os
import logging

from flask_cors import CORS
from apiflask import APIFlask

from routes import legacy, v1

logging.getLogger().setLevel(logging.INFO)

app = APIFlask(
    __name__,
    title="Celatone API",
    version="1.0",
    spec_path="/openapi.yml",
    docs_ui="swagger-ui",
)
app.config["SYNC_LOCAL_SPEC"] = True
app.config["LOCAL_SPEC_PATH"] = os.path.join(app.root_path, "openapi.json")

app.register_blueprint(legacy.legacy_bp)
app.register_blueprint(v1.v1_bp, url_prefix="/v1")

CORS(app)


@app.route("/", methods=["GET"])
def hello_world():
    return {"gm": "gm"}


@app.errorhandler(500)
def handle_500_error(error):
    return {"error": "Internal Server Error"}, 500


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("FLASK_DEBUG", True),
        host=os.environ.get("FLASK_HOST", "0.0.0.0"),
        port=int(os.environ.get("FLASK_PORT", 8080)),
    )
