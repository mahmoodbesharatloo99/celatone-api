import requests

from utils.gcs import get_network_data
from utils.graphql.common import get_graphql_health


def generate_health(chain, network, check, checks):
    if check not in checks:
        checks[check] = {}
    if chain not in checks[check]:
        checks[check][chain] = {}
    if network not in checks[check][chain]:
        checks[check][chain][network] = {}


def check_status(chain, network, check, checks, response, block_path):
    status = "ok"
    try:
        if response.status_code == 200:
            response = response.json()
            checks[check][chain][network]["status"] = "ok"
            for path in block_path:
                response = response[path]
            checks[check][chain][network]["block"] = str(response)
    except requests.exceptions.RequestException as e:
        checks[check][chain][network]["status"] = "error"
        checks[check][chain][network]["error"] = str(e)
        status = "error"
    return checks, status


def lcd_check(chain, network, checks):
    response = requests.get(f"{get_network_data(chain,network,'lcd')}/blocks/latest")
    block_path = ["block", "header", "height"]
    return check_status(chain, network, "lcd", checks, response, block_path)


def graphql_check(chain, network, checks):
    response = get_graphql_health(chain, network)
    block_path = ["data", "blocks", 0, "height"]
    return check_status(chain, network, "graphql", checks, response, block_path)


def health_check(chain, network):
    health = {}
    checks = health["checks"] = {}
    status = "ok"
    generate_health(chain, network, "lcd", checks)
    generate_health(chain, network, "graphql", checks)
    checks, lcd_status = lcd_check(chain, network, checks)
    checks, graphql_status = graphql_check(chain, network, checks)
    if lcd_status == "error" or graphql_status == "error":
        status = "error"
    health["status"] = status
    return health
