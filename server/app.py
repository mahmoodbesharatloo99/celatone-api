import os

from flask_cors import CORS
from apiflask import APIFlask

from routes import accounts, assets, cosmwasm, monitoring, icns, misc, registry, staking, transactions

app = APIFlask(__name__, title="Celatone API", version="1.0")

app.register_blueprint(accounts.accounts_bp)
app.register_blueprint(assets.assets_bp)
app.register_blueprint(cosmwasm.cosmwasm_bp)
app.register_blueprint(monitoring.monitoring_bp)
app.register_blueprint(icns.icns_bp)
app.register_blueprint(misc.misc_bp)
app.register_blueprint(registry.registry_bp)
app.register_blueprint(staking.staking_bp)
app.register_blueprint(transactions.transactions_bp)

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
