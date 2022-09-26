import pytest
from app import app
from flask import appcontext_pushed, g, json, jsonify, Flask

# from flask_pytest_example.handlers.routes import configure_routes


info_user = [
    {
        "DoB": "2000-07-31",
        "creditcard": " ",
        "email": "bleh1@gmail.com",
        "password": "coolIsmad2",
        "username": "ever",
    }
]


@pytest.fixture
def client():
    return app.test_client()


def test_reg(client):
    resp = client.post(
        "/user",
        json={
            "DoB": "2000-07-31",
            "creditcard": " ",
            "email": "bleh1@gmail.com",
            "password": "coolIsmad2",
            "username": "ever5",
        },
    )
    assert resp.status_code == 201


def test_reg_same_username(client):
    resp = client.post(
        "/user",
        json={
            "DoB": "2000-07-31",
            "creditcard": "5555555555554433",
            "email": "bleh1@gmail.com",
            "password": "coolIsmad2",
            "username": "ever5",
        },
    )
    assert resp.status_code == 409


def test_reg_underage(client):
    resp = client.post(
        "/user",
        json={
            "DoB": "2010-07-31",
            "creditcard": " ",
            "email": "bleh1@gmail.com",
            "password": "coolIsmad2",
            "username": "prime2",
        },
    )
    assert resp.status_code == 403


def test_reg_invalid_info(client):
    resp = client.post(
        "/user",
        json={
            "DoB": "2000-07-31",
            "creditcard": "4444",
            "email": "prize3@gmail.com",
            "password": "coolIsmad2",
            "username": "reply_the_glue",
        },
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 400


# ?
# @app.route('/user')
# def users_me():
#  return jsonify(username=g.user.name)


def get_request_registered_users(client):
    resp = client.get(
        "/user",
        json={
            "DoB": "2000-07-31",
            "creditcard": "4444",
            "email": "prize3@gmail.com",
            "password": "coolIsmad2",
            "username": "reply_the_glue",
        },
        headers={"Content-Type": "application/json"},
    )
    # assert isinstance(resp.get_json(), dict)
    assert resp.status_code == 200


# assert resp.json.get(resp.data)
#

# http://127.0.0.1:5000/user?DoB={}&creditcard={}&email={}&password={}&username={}
# def test_base_route(client):
# response = app.test_client().get(
#     "/user?username=sabsthenabs12&password=CplusplusisAmazing12&email=randomemail1@gmail.com&DoB=2000-07-31&creditcard=N/A"
# )
# assert response.status_code == 400
# assert json.dumps(response.data) == info_user


# assert b"No entries here so far" in response.data
# assert response.json() == info_user
# assert response.status_code == 200


def test_payment(client):

    resp = client.post(
        "/payment",
        json={"credit_card_number": "5555555555554444", "Amount": "150"},
    )
    assert resp.status_code == 201


def test_payment_invalid_amount(client):
    resp = client.post(
        "/payment",
        json={"credit_card_number": "5555555555554444", "Amount": "15"},
    )
    assert resp.status_code == 400


def test_payment_invalid_user(client):
    resp = client.post(
        "/payment",
        json={"credit_card_number": "3776873370917133", "Amount": "150"},
    )
    assert resp.status_code == 404
