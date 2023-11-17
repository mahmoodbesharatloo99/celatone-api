import json
import logging
import os

from apiflask import APIFlask
from flask_cors import CORS
from routes import legacy, v1
from werkzeug.exceptions import HTTPException

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


@app.errorhandler(HTTPException)
@app.errorhandler(Exception)
def handle_exception(e: Exception):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    # now you're handling non-HTTP exceptions only
    return {
        "code": 500,
        "description": str(e),
    }, 500


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("FLASK_DEBUG", True),
        host=os.environ.get("FLASK_HOST", "0.0.0.0"),
        port=int(os.environ.get("FLASK_PORT", 8080)),
    )
