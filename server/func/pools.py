from func.registry import load_and_check_registry_data


def get_pools(chain, network):
    pools = load_and_check_registry_data(chain, network, "pools")
    return pools


def get_pool(chain, network, pool_id):
    pools = get_pools(chain, network)
    pool = next(filter(lambda pool: pool["id"] == int(pool_id), pools), None)
    return pool