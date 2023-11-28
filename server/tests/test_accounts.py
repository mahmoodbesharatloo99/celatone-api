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


def test_get_account_table_count():
    chain = "osmosis"
    network = "osmo-test-5"
    account_address = "osmo1acqpnvg2t4wmqfdv8hq47d3petfksjs5r9t45p"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{account_address}/table-count"
    )
    assert response.status_code == 200

    response_json = response.get_json()
    assert type(response_json["tx"]) == int
    assert type(response_json["proposal"]) == int
    assert "code" not in response_json
    assert "instantiated" not in response_json
    assert "contract_by_admin" not in response_json


def test_get_account_table_count_wasm():
    chain = "osmosis"
    network = "osmo-test-5"
    account_address = "osmo1acqpnvg2t4wmqfdv8hq47d3petfksjs5r9t45p"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{account_address}/table-count?is_wasm=true"
    )
    assert response.status_code == 200

    response_json = response.get_json()
    assert type(response_json["tx"]) == int
    assert type(response_json["proposal"]) == int
    assert type(response_json["code"]) == int
    assert type(response_json["instantiated"]) == int
    assert type(response_json["contract_by_admin"]) == int


def test_get_account_table_count_new_address():
    chain = "osmosis"
    network = "osmo-test-5"
    account_address = "osmo14wk9zecqam9jsac7xwtf8e349ckquzzlx9k8c3"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{account_address}/table-count?is_wasm=true"
    )
    assert response.status_code == 200


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

    assert type(response_json["total"]) == int


def test_get_admin_contracts():
    chain = "osmosis"
    network = "osmo-test-5"
    limit = 10
    offset = 0
    address = "osmo1acqpnvg2t4wmqfdv8hq47d3petfksjs5r9t45p"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/wasm/admin-contracts?limit={limit}&offset={offset}"
    )
    assert response.status_code == 200

    response_json = response.json

    for item in response_json["items"]:
        assert type(item["contract_address"]) == str
        assert type(item["label"]) == str
        assert type(item["admin"]) == str
        assert type(item["instantiator"]) == str
        assert type(item["latest_updated"]) == str
        assert type(item["latest_updater"]) == str
        remark = item["remark"]
        assert type(remark["operation"]) == str
        assert type(remark["type"]) == str
        assert type(remark["value"]) == str

    assert type(response_json["total"]) == int


def test_get_instatiated_contracts():
    chain = "osmosis"
    network = "osmo-test-5"
    limit = 10
    offset = 0
    address = "osmo1acqpnvg2t4wmqfdv8hq47d3petfksjs5r9t45p"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/wasm/instantiated-contracts?limit={limit}&offset={offset}"
    )
    assert response.status_code == 200

    response_json = response.json

    for item in response_json["items"]:
        assert type(item["contract_address"]) == str
        assert type(item["label"]) == str
        assert type(item["admin"]) == str or item["admin"] is None
        assert type(item["instantiator"]) == str
        assert type(item["latest_updated"]) == str
        assert type(item["latest_updater"]) == str
        remark = item["remark"]
        assert type(remark["operation"]) == str
        assert type(remark["type"]) == str
        assert type(remark["value"]) == str

    assert type(response_json["total"]) == int


def test_get_codes():
    chain = "osmosis"
    network = "osmo-test-5"
    limit = 10
    offset = 0
    address = "osmo1acqpnvg2t4wmqfdv8hq47d3petfksjs5r9t45p"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/wasm/codes?limit={limit}&offset={offset}"
    )
    assert response.status_code == 200

    response_json = response.json

    for item in response_json["items"]:
        assert type(item["id"]) == int
        assert type(item["cw2_contract"]) == str or item["cw2_contract"] is None
        assert type(item["cw2_version"]) == str or item["cw2_version"] is None
        assert type(item["uploader"]) == str
        assert type(item["contract_count"]) == int
        assert type(item["instantiate_permission"]) == str
        assert type(item["permission_addresses"]) == list

    assert type(response_json["total"]) == int


def test_get_move_resources():
    chain = "initia"
    network = "stone-11"
    address = "init1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqpqr5e3d"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/move/resources"
    )
    assert response.status_code == 200

    response_json = response.json

    for item in response_json["items"]:
        assert type(item["address"]) == str
        assert type(item["move_resource"]) == str
        assert type(item["raw_bytes"]) == str
        assert type(item["struct_tag"]) == str

    assert type(response_json["total"]) == int


def test_get_move_resources_invalid_chain():
    chain = "osmosis"
    network = "osmo-test-5"
    address = "osmo1acqpnvg2t4wmqfdv8hq47d3petfksjs5r9t45p"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/move/resources"
    )
    assert response.status_code == 404


def test_get_move_modules():
    chain = "initia"
    network = "stone-11"
    address = "init1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqpqr5e3d"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/move/modules"
    )
    assert response.status_code == 200

    response_json = response.json

    for item in response_json["items"]:
        assert type(item["abi"]) == str
        assert type(item["address"]) == str
        assert type(item["module_name"]) == str
        assert type(item["raw_bytes"]) == str
        assert type(item["upgrade_policy"]) == str

    assert type(response_json["total"]) == int


def test_get_move_modules_invalid_chain():
    chain = "osmosis"
    network = "osmo-test-5"
    address = "osmo1acqpnvg2t4wmqfdv8hq47d3petfksjs5r9t45p"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/move/modules"
    )
    assert response.status_code == 404
