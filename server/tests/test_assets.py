from app import app


def test_assets():
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


def test_assets_with_prices_false():
    chain = "osmosis"
    network = "osmosis-1"

    response = app.test_client().get(f"/v1/{chain}/{network}/assets?with_prices=false")
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


def test_assets_with_prices_true():
    chain = "osmosis"
    network = "osmosis-1"

    non_zero_price = False

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
        non_zero_price = non_zero_price or asset["price"] > 0
    assert non_zero_price == True


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
