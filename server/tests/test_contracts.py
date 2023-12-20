from app import app


def test_get_contract_table_counts():
    chain = "osmosis"
    network = "osmosis-1"
    contract_address = "osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/contracts/{contract_address}/table-counts"
    )
    assert response.status_code == 200

    response_json = response.get_json()
    assert type(response_json["tx"]) == int
    assert type(response_json["migration"]) == int
    assert "related_proposal" not in response_json


def test_get_contract_table_counts_gov():
    chain = "osmosis"
    network = "osmosis-1"
    contract_address = "osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/contracts/{contract_address}/table-counts?is_gov=true"
    )
    assert response.status_code == 200

    response_json = response.get_json()
    assert type(response_json["tx"]) == int
    assert type(response_json["migration"]) == int
    assert type(response_json["related_proposal"]) == int


def test_get_migrations():
    chain = "osmosis"
    network = "osmo-test-5"
    contract_address = "osmo16rg8mzgn899253w5jfe3wgdx3eugx4vucw7lgsvm737xlnnyz56sanpz0g"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/contracts/{contract_address}/migrations?limit=10&offset=0"
    )
    assert response.status_code == 200

    response_json = response.get_json()
    for migration in response_json["items"]:
        assert type(migration["code_id"]) == int
        assert type(migration["sender"]) == str
        assert type(migration["height"]) == int
        assert type(migration["timestamp"]) == str
        assert (
            migration["remark"]["operation"]
            == "CONTRACT_CODE_HISTORY_OPERATION_TYPE_INIT"
            or migration["remark"]["operation"]
            == "CONTRACT_CODE_HISTORY_OPERATION_TYPE_MIGRATE"
            or migration["remark"]["operation"]
            == "CONTRACT_CODE_HISTORY_OPERATION_TYPE_GENESIS"
        )
        assert (
            migration["remark"]["type"] == "genesis"
            or migration["remark"]["type"] == "governance"
            or migration["remark"]["type"] == "transaction"
        )
        assert (
            type(migration["remark"]["value"]) == str
            or type(migration["remark"]["value"]) == int
        )
        assert type(migration["uploader"]) == str
        assert type(migration["cw2_contract"]) == str
        assert type(migration["cw2_version"]) == str


def test_get_related_proposals():
    chain = "osmosis"
    network = "osmosis-1"
    contract_address = "osmo1k8re7jwz6rnnwrktnejdwkwnncte7ek7gt29gvnl3sdrg9mtnqkse6nmqm"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/contracts/{contract_address}/related-proposals?limit=10&offset=0"
    )
    assert response.status_code == 200

    response_json = response.get_json()
    for migration in response_json["items"]:
        assert type(migration["proposal_id"]) == int
        assert type(migration["title"]) == str
        assert type(migration["status"]) == str
        assert type(migration["voting_end_time"]) == str
        assert type(migration["deposit_end_time"]) == str
        assert type(migration["resolved_height"]) == int
        assert type(migration["type"]) == str
        assert type(migration["proposer"]) == str
        assert type(migration["is_expedited"]) == bool


def test_get_contract_states():
    chain = "osmosis"
    network = "osmo-test-5"
    contract_address = "osmo16rg8mzgn899253w5jfe3wgdx3eugx4vucw7lgsvm737xlnnyz56sanpz0g"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/contracts/{contract_address}/states?limit=100"
    )
    assert response.status_code == 200

    response_json = response.get_json()
    for pair in response_json["models"]:
        assert type(pair["key"]) == str
        assert type(pair["value"]) == str
    assert response_json["pagination"]["next_key"] == None


def test_get_contract_states_pagination_key():
    chain = "osmosis"
    network = "osmo-test-5"
    contract_address = "osmo16rg8mzgn899253w5jfe3wgdx3eugx4vucw7lgsvm737xlnnyz56sanpz0g"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/contracts/{contract_address}/states?limit=2"
    )
    assert response.status_code == 200

    response_1 = app.test_client().get(
        f"/v1/{chain}/{network}/contracts/{contract_address}/states?limit=1"
    )
    assert response_1.status_code == 200
    next_key = response_1.get_json()["pagination"]["next_key"]

    response_2 = app.test_client().get(
        f"/v1/{chain}/{network}/contracts/{contract_address}/states?limit=1&pagination_key={next_key}"
    )
    assert response_2.status_code == 200

    assert (
        response.get_json()["pagination"]["next_key"]
        == response_2.get_json()["pagination"]["next_key"]
    )
