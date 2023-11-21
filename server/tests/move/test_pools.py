from app import app


def test_get_account_info_failed():
    chain = "initia"
    network = "stone-11"

    response = app.test_client().get(f"/v1/{chain}/{network}/move/pools")
    assert response.status_code == 200

    for pool in response.json:
        for coin in ["coin_a", "coin_b"]:
            coin_info = pool[coin]
            assert type(coin_info["metadata"]) == str
            assert type(coin_info["denom"]) == str
            assert type(coin_info["decimals"]) == int
            assert type(pool[f"{coin}_weight"]) == str
            assert type(pool[f"{coin}_amount"]) == str
        assert type(pool["liquidity_token"]["metadata"]) == str
        assert type(pool["liquidity_token"]["denom"]) == str
        assert type(pool["liquidity_token"]["decimals"]) == int
        assert type(pool["total_share"]) == str
