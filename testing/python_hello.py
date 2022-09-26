msg = "hello"
print(msg)

from app import app
import pytest
import json


@pytest.fixture
def client():
    return app.test_client()


def test_base_route(client):
    response = client.get("/user")
    print(response)


test_base_route(client)
