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
