from app import app


def test_assets_without_prices():
    chain = "osmosis"
    network = "osmosis-1"

    response = app.test_client().get(f"/v1/{chain}/{network}/assets")
    assert response.status_code == 200

    for asset in response.json:
        assert type(asset["coingecko"]) == str
        assert type(asset["description"]) == str
        assert type(asset["id"]) == str
        assert type(asset["logo"]) == str
        assert type(asset["name"]) == str
        assert type(asset["precision"]) == int
        assert type(asset["price"]) == float
        assert type(asset["slugs"]) == list
        assert type(asset["symbol"]) == str
        assert type(asset["type"]) == str


def test_assets_with_prices():
    chain = "osmosis"
    network = "osmosis-1"

    response = app.test_client().get(f"/v1/{chain}/{network}/assets?with_prices=true")
    assert response.status_code == 200

    for asset in response.json:
        assert type(asset["coingecko"]) == str
        assert type(asset["description"]) == str
        assert type(asset["id"]) == str
        assert type(asset["logo"]) == str
        assert type(asset["name"]) == str
        assert type(asset["precision"]) == int
        assert type(asset["price"]) == float
        assert type(asset["slugs"]) == list
        assert type(asset["symbol"]) == str
        assert type(asset["type"]) == str


def test_assets_type():
    chain = "osmosis"
    network = "osmosis-1"

    for type in ["natives", "cw20", "ibc"]:
        response = app.test_client().get(f"/v1/{chain}/{network}/assets/type/{type}")
        assert response.status_code == 200

        for asset in response.json:
            assert type(asset["coingecko"]) == str
            assert type(asset["description"]) == str
            assert type(asset["id"]) == str
            assert type(asset["logo"]) == str
            assert type(asset["name"]) == str
            assert type(asset["precision"]) == int
            assert type(asset["price"]) == float
            assert type(asset["slugs"]) == list
            assert type(asset["symbol"]) == str
            assert asset["type"] == type
