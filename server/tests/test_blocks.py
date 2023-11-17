from app import app

chain = "osmosis"
network = "osmosis-1"
limit = 10
offset = 0


def test_blocks():
    response = app.test_client().get(
        f"/v1/{chain}/{network}/blocks?limit={limit}&offset={offset}"
    )
    assert response.status_code == 200

    response_json = response.json
    assert len(response_json["items"]) == limit
    assert type(response_json["total"]) == int

    item = response_json["items"][0]
    assert type(item["hash"]) == str
    assert type(item["height"]) == int
    assert type(item["timestamp"]) == str
    assert type(item["transaction_count"]) == int
    assert type(item["validator"]["moniker"]) == str
    assert type(item["validator"]["operator_address"]) == str
    assert type(item["validator"]["identity"]) == str
