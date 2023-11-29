from app import app


def test_get_account_info():
    chain = "osmosis"
    network = "osmosis-1"

    response = app.test_client().get(f"/v1/{chain}/{network}/overviews/stats")
    assert response.status_code == 200

    response_json = response.get_json()
    assert type(response_json["block_time"]) == float
    assert type(response_json["latest_block"]["height"]) == int
    assert type(response_json["latest_block"]["timestamp"]) == str
    assert type(response_json["transaction_count"]) == int
