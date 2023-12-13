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
        assert type(item["height"]) == int
        assert type(item["latest_updated"]) == str
        assert type(item["is_republished"]) == bool
        assert type(item["is_verified"]) == bool


def test_move_modules_transactions():
    chain = "initia"
    network = "stone-12-1"
    limit = 10
    offset = 0
    vm_address = "0x1"
    name = "coin"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/move/modules/{vm_address}/{name}/txs?limit={limit}&offset={offset}"
    )
    assert response.status_code == 200

    response_json = response.json

    for item in response_json["items"]:
        assert type(item["height"]) == int
        assert type(item["created"]) == str
        assert type(item["sender"]) == str
        assert type(item["hash"]) == str
        assert type(item["success"]) == bool
        assert type(item["messages"]) == list
        assert type(item["is_send"]) == bool
        assert type(item["is_ibc"]) == bool
        assert type(item["is_move_publish"]) == bool
        assert type(item["is_move_upgrade"]) == bool
        assert type(item["is_move_execute"]) == bool
        assert type(item["is_move_script"]) == bool
        assert item.get("is_opinit") == None


def test_move_modules_transactions_initia():
    chain = "initia"
    network = "stone-12-1"
    limit = 10
    offset = 0
    vm_address = "0x1"
    name = "coin"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/move/modules/{vm_address}/{name}/txs?limit={limit}&offset={offset}&is_initia=true"
    )
    assert response.status_code == 200

    response_json = response.json

    for item in response_json["items"]:
        assert type(item["is_opinit"]) == bool


def test_move_modules_transactions_invalid_vm_address():
    chain = "initia"
    network = "stone-12-1"
    limit = 10
    offset = 0
    vm_address = "0x2"
    name = "coin"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/move/modules/{vm_address}/{name}/txs?limit={limit}&offset={offset}&is_initia=true"
    )
    assert response.status_code == 200
    assert response.json["items"] == []


def test_move_modules_transactions_invalid_name():
    chain = "initia"
    network = "stone-12-1"
    limit = 10
    offset = 0
    vm_address = "0x1"
    name = "beeb"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/move/modules/{vm_address}/{name}/txs?limit={limit}&offset={offset}&is_initia=true"
    )
    assert response.status_code == 200
    assert response.json["items"] == []