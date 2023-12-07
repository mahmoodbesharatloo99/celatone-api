from app import app
import pytest


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


def test_get_transactions():
    chain = "osmosis"
    network = "osmo-test-5"
    limit = 10
    offset = 0
    address = "osmo1acqpnvg2t4wmqfdv8hq47d3petfksjs5r9t45p"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/txs?limit={limit}&offset={offset}"
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

    assert type(response_json["total"]) == int


def test_get_transactions_invalid_address():
    chain = "osmosis"
    network = "osmo-test-5"
    limit = 10
    offset = 0
    address = "invalid_address"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/txs?limit={limit}&offset={offset}"
    )
    assert response.status_code == 200
    assert response.json["total"] == 0
    assert response.json["items"] == []


def test_get_transactions_wasm():
    chain = "osmosis"
    network = "osmo-test-5"
    limit = 10
    offset = 0
    address = "osmo1acqpnvg2t4wmqfdv8hq47d3petfksjs5r9t45p"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/txs?limit={limit}&offset={offset}&is_wasm=true"
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
        assert type(item["is_clear_admin"]) == bool
        assert type(item["is_execute"]) == bool
        assert type(item["is_instantiate"]) == bool
        assert type(item["is_migrate"]) == bool
        assert type(item["is_store_code"]) == bool
        assert type(item["is_update_admin"]) == bool

    assert type(response_json["total"]) == int


def test_get_transactions_move():
    chain = "initia"
    network = "stone-11"
    limit = 10
    offset = 0
    address = "init1acqpnvg2t4wmqfdv8hq47d3petfksjs59gckf3"

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/txs?limit={limit}&offset={offset}&is_move=true"
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

    assert type(response_json["total"]) == int


def test_get_transactions_only_signer():
    chain = "osmosis"
    network = "osmo-test-5"
    limit = 10
    offset = 0
    address = "osmo1acqpnvg2t4wmqfdv8hq47d3petfksjs5r9t45p"
    is_signer = True

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/txs?limit={limit}&offset={offset}&is_signer={is_signer}"
    )
    assert response.status_code == 200

    response_json = response.json

    for item in response_json["items"]:
        assert item["is_signer"] == is_signer


def test_get_transactions_only_related():
    chain = "osmosis"
    network = "osmo-test-5"
    limit = 10
    offset = 0
    address = "osmo1acqpnvg2t4wmqfdv8hq47d3petfksjs5r9t45p"
    is_signer = False

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/txs?limit={limit}&offset={offset}&is_signer={is_signer}"
    )
    assert response.status_code == 200

    response_json = response.json

    for item in response_json["items"]:
        assert item["is_signer"] == is_signer


def test_get_transactions_filters():
    chain = "osmosis"
    network = "osmo-test-5"
    limit = 10
    offset = 0
    address = "osmo1acqpnvg2t4wmqfdv8hq47d3petfksjs5r9t45p"
    is_send = True

    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/txs?limit={limit}&offset={offset}&is_send={is_send}"
    )
    for item in response.json["items"]:
        assert item["is_send"] == is_send

    is_wasm = True
    is_store_code = True
    is_execute = True
    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/txs?limit={limit}&offset={offset}&is_wasm={is_wasm}&is_store_code={is_store_code}&is_execute={is_execute}"
    )
    for item in response.json["items"]:
        assert item["is_store_code"] == is_store_code
        assert item["is_execute"] == is_execute


@pytest.mark.parametrize(
    "chain, network, address",
    [
        ("osmosis", "osmosis-1", "osmo1acqpnvg2t4wmqfdv8hq47d3petfksjs5r9t45p"),
        ("osmosis", "osmosis-1", "osmo1j0vaeh27t4rll7zhmarwcuq8xtrmvqhuqv0av9"),
        # TODO: update to stone-12 later
        ("initia", "stone-11", "init1acqpnvg2t4wmqfdv8hq47d3petfksjs59gckf3"),
        ("initia", "stone-11", "init1k9dcrj33flyru4jz4pq6tydadegpdj3whu3wax"),
    ],
)
def test_get_delegations(chain, network, address):
    response = app.test_client().get(
        f"/v1/{chain}/{network}/accounts/{address}/delegations"
    )
    assert response.status_code == 200

    response_json = response.json

    # is_validator
    assert type(response_json["is_validator"]) == bool

    # staking params
    staking_params = response_json["staking_params"]
    assert type(staking_params["bond_denoms"]) == list
    for denom in staking_params["bond_denoms"]:
        assert type(denom) == str
    assert type(staking_params["historical_entries"]) == int
    assert type(staking_params["max_entries"]) == int
    assert type(staking_params["max_validators"]) == int
    assert type(staking_params["min_commission_rate"]) == str
    assert type(staking_params["unbonding_time"]) == str

    # delegations
    for item in response_json["delegations"]:
        assert type(item["balance"]) == list
        for balance in item["balance"]:
            assert type(balance["amount"]) == str
            assert type(balance["denom"]) == str
        assert type(item["validator"]) == dict
        assert type(item["validator"]["validator_address"]) == str
        assert (
            type(item["validator"]["moniker"]) == str
            or item["validator"]["moniker"] is None
        )
        assert (
            type(item["validator"]["identity"]) == str
            or item["validator"]["identity"] is None
        )

    # unbondings
    for item in response_json["unbondings"]:
        assert type(item["entries"]) == list
        for entry in item["entries"]:
            assert type(entry["balance"]) == list
            for balance in entry["balance"]:
                assert type(balance["amount"]) == str
                assert type(balance["denom"]) == str
            assert type(entry["completion_time"]) == str
            assert type(entry["creation_height"]) == str
            assert type(entry["initial_balance"]) == list
            for balance in entry["initial_balance"]:
                assert type(balance["amount"]) == str
                assert type(balance["denom"]) == str
        assert type(item["validator"]) == dict
        assert type(item["validator"]["validator_address"]) == str
        assert (
            type(item["validator"]["moniker"]) == str
            or item["validator"]["moniker"] is None
        )
        assert (
            type(item["validator"]["identity"]) == str
            or item["validator"]["identity"] is None
        )

    # redelegations
    for item in response_json["redelegations"]:
        assert type(item["entries"]) == list
        for entry in item["entries"]:
            assert type(entry["balance"]) == list
            for balance in entry["balance"]:
                assert type(balance["amount"]) == str
                assert type(balance["denom"]) == str
            assert type(entry["redelegation_entry"]) == dict
            assert type(entry["redelegation_entry"]["completion_time"]) == str
            assert type(entry["redelegation_entry"]["creation_height"]) == int
            assert type(entry["redelegation_entry"]["initial_balance"]) == list
            for balance in entry["redelegation_entry"]["initial_balance"]:
                assert type(balance["amount"]) == str
                assert type(balance["denom"]) == str
            assert type(entry["redelegation_entry"]["shares_dst"]) == list
            for balance in entry["redelegation_entry"]["shares_dst"]:
                assert type(balance["amount"]) == str
                assert type(balance["denom"]) == str
        assert type(item["validator_dst"]) == dict
        assert type(item["validator_dst"]["validator_address"]) == str
        assert (
            type(item["validator_dst"]["moniker"]) == str
            or item["validator_dst"]["moniker"] is None
        )
        assert (
            type(item["validator_dst"]["identity"]) == str
            or item["validator_dst"]["identity"] is None
        )
        assert type(item["validator_src"]) == dict
        assert type(item["validator_src"]["validator_address"]) == str
        assert (
            type(item["validator_src"]["moniker"]) == str
            or item["validator_src"]["moniker"] is None
        )
        assert (
            type(item["validator_src"]["identity"]) == str
            or item["validator_src"]["identity"] is None
        )

    # rewards
    delegations_rewards = response_json["delegations_rewards"]
    assert type(delegations_rewards["total"]) == list
    for balance in delegations_rewards["total"]:
        assert type(balance["amount"]) == str
        assert type(balance["denom"]) == str
    for item in delegations_rewards["rewards"]:
        assert type(item["reward"]) == list
        for balance in item["reward"]:
            assert type(balance["amount"]) == str
            assert type(balance["denom"]) == str
        assert type(item["validator"]) == dict
        assert type(item["validator"]["validator_address"]) == str
        assert (
            type(item["validator"]["moniker"]) == str
            or item["validator"]["moniker"] is None
        )
        assert (
            type(item["validator"]["identity"]) == str
            or item["validator"]["identity"] is None
        )

    # commission
    for balance in response_json["commissions"]:
        assert type(balance["amount"]) == str
        assert type(balance["denom"]) == str
