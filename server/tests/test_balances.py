from app import app


def test_balances():
    chain = "terra"
    network = "phoenix-1"
    account = "terra1m9zy077gv3h6076nkardvfmuvyf2pez6ny0wr0"

    response = app.test_client().get(f"/v1/{chain}/{network}/balances/{account}")
    assert response.status_code == 200

    for balance in response.json:
        assert type(balance["denom"]) == str
        assert type(balance["amount"]) == str
