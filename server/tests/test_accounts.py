from app import app


def test_get_account_info():
    chain = "osmosis"
    network = "osmosis-1"
    account_address = "osmo18kmnpjw6mj7juw6wmnzdyaa8e2tg9h3mqry0ym"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{account_address}/info"
    )
    assert response.status_code == 200

    response_json = response.get_json()
    assert "icns" in response_json
    assert "project_info" in response_json
    assert "public_info" in response_json


def test_get_account_info_failed():
    chain = "osmosis"
    network = "osmosis-1"
    account_address = "invalid_address"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{account_address}/info"
    )
    assert response.status_code == 500


def test_get_proposals_by_address():
    chain = "osmosis"
    network = "osmo-test-5"
    limit = 10
    offset = 0
    address = "osmo1acqpnvg2t4wmqfdv8hq47d3petfksjs5r9t45p"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/proposals?limit={limit}&offset={offset}"
    )
    assert response.status_code == 200

    response_json = response.json

    for item in response_json["items"]:
        assert type(item["deposit_end_time"]) == str
        assert type(item["id"]) == int
        assert type(item["is_expedited"]) == bool
        assert type(item["resolved_height"]) == int
        assert type(item["status"]) == str
        assert type(item["title"]) == str
        assert type(item["type"]) == str
        assert type(item["voting_end_time"]) == str
