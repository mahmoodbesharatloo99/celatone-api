from app import app


def test_transactions_wasm():
    chain = "osmosis"
    network = "osmosis-1"
    limit = 10
    offset = 0

    response = app.test_client().get(
        f"/v1/{chain}/{network}/txs?limit={limit}&offset={offset}&is_wasm=true"
    )
    assert response.status_code == 200

    response_json = response.json
    assert len(response_json["items"]) == limit
    assert type(response_json["total"]) == int

    for item in response_json["items"]:
        assert type(item["height"]) == int
        assert type(item["created"]) == str
        assert type(item["hash"]) == str
        assert type(item["sender"]) == str
        assert type(item["success"]) == bool
        assert type(item["messages"]) == list
        assert type(item["is_send"]) == bool
        assert type(item["is_ibc"]) == bool
        assert type(item["is_clear_admin"]) == bool
        assert type(item["is_execute"]) == bool
        assert type(item["is_instantiate"]) == bool
        assert type(item["is_migrate"]) == bool
        assert type(item["is_store_code"]) == bool
        assert type(item["is_update_admin"]) == bool
        assert item.get("is_move_publish") is None
        assert item.get("is_move_upgrade") is None
        assert item.get("is_move_execute") is None
        assert item.get("is_move_script") is None


def test_transactions_move():
    chain = "initia"
    network = "stone-11"
    limit = 10
    offset = 0

    response = app.test_client().get(
        f"/v1/{chain}/{network}/txs?limit={limit}&offset={offset}&is_move=true"
    )
    assert response.status_code == 200

    response_json = response.json
    assert len(response_json["items"]) == limit
    assert type(response_json["total"]) == int

    for item in response_json["items"]:
        assert type(item["height"]) == int
        assert type(item["created"]) == str
        assert type(item["hash"]) == str
        assert type(item["sender"]) == str
        assert type(item["success"]) == bool
        assert type(item["messages"]) == list
        assert type(item["is_send"]) == bool
        assert type(item["is_ibc"]) == bool
        assert item.get("is_clear_admin") is None
        assert item.get("is_execute") is None
        assert item.get("is_instantiate") is None
        assert item.get("is_migrate") is None
        assert item.get("is_store_code") is None
        assert item.get("is_update_admin") is None
        assert type(item["is_move_publish"]) == bool
        assert type(item["is_move_upgrade"]) == bool
        assert type(item["is_move_execute"]) == bool
        assert type(item["is_move_script"]) == bool


def test_transactions_initia():
    chain = "initia"
    network = "stone-12-1"
    limit = 10
    offset = 0

    response = app.test_client().get(
        f"/v1/{chain}/{network}/txs?limit={limit}&offset={offset}&is_initia=true"
    )
    assert response.status_code == 200

    response_json = response.json
    assert len(response_json["items"]) == limit
    assert type(response_json["total"]) == int

    for item in response_json["items"]:
        assert type(item["block"]["height"]) == int
        assert type(item["block"]["timestamp"]) == str
        assert type(item["hash"]) == str
        assert type(item["success"]) == bool
        assert type(item["messages"]) == list
        assert type(item["is_send"]) == bool
        assert type(item["is_ibc"]) == bool
        assert type(item["is_opinit"]) == bool


def test_transaction():
    chain = "osmosis"
    network = "osmosis-1"
    tx_hash = "1871395F6BAF39725360BC11D984887A1918BBE140E5C760780B2309A58A57FC"

    response = app.test_client().get(f"/v1/{chain}/{network}/txs/{tx_hash}")
    assert response.status_code == 200

    response_json = response.json
    assert response_json["tx"] is not None
    assert response_json["tx_response"] is not None


def test_transaction_invalid():
    chain = "osmosis"
    network = "osmosis-1"
    tx_hash = "4672E1FBAED630BC3C0A5CD4703BB6FCD9F9CC9FD618DDAFBCB650610761B6B8"

    response = app.test_client().get(f"/v1/{chain}/{network}/txs/{tx_hash}")
    assert response.status_code == 404
