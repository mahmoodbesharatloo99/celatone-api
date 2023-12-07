from app import app


def test_move_modules():
    chain = "initia"
    network = "stone-12-1"
    limit = 10
    offset = 0

    response = app.test_client().get(
        f"/v1/{chain}/{network}/move/modules?limit={limit}&offset={offset}"
    )
    assert response.status_code == 200

    response_json = response.json
    assert len(response_json["items"]) == limit
    assert type(response_json["total"]) == int

    for item in response_json["items"]:
        assert type(item["name"]) == str
        assert type(item["address"]) == str
        assert type(item["block"]["height"]) == int
        assert type(item["block"]["timestamp"]) == str
        assert type(item["is_republish"]) == bool
        assert type(item["is_verify"]) == bool
