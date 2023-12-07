from app import app


def test_get_overviews_stats():
    chain = "sei"
    network = "pacific-1"

    response = app.test_client().get(f"/v1/{chain}/{network}/overviews/stats")
    assert response.status_code == 200

    response_json = response.get_json()
    assert type(response_json["block_time"]) == float
    assert type(response_json["latest_block"]) == int
    assert type(response_json["transaction_count"]) == int


def test_get_overviews_stats_legacy():
    chain = "osmosis"
    network = "osmosis-1"

    response = app.test_client().get(f"/v1/{chain}/{network}/overviews/stats")
    assert response.status_code == 200

    response_json = response.get_json()
    assert type(response_json["block_time"]) == float
    assert type(response_json["latest_block"]) == int
    assert type(response_json["transaction_count"]) == int


def test_get_overviews_stats_invalid_network():
    chain = "alles"
    network = "celatone-1"

    response = app.test_client().get(f"/v1/{chain}/{network}/overviews/stats")
    assert response.status_code == 200

    response_json = response.get_json()
    assert response_json["block_time"] == None
    assert response_json["latest_block"] == None
    assert response_json["transaction_count"] == None
