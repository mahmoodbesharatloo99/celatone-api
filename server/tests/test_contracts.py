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
    assert type(response_json["related_proposal"]) == int
