import os
import pytest

from api.booking_client import BookingClient


def pytest_addoption(parser):
    parser.addoption("--env", default="prod", choices=["prod", "local"])


URLS = {
    "prod": "https://restful-booker.herokuapp.com",
    "local": "http://localhost:3001"
}


@pytest.fixture(scope="session")
def base_url(request):
    env = request.config.getoption("--env")
    return URLS[env]


@pytest.fixture(scope="session")
def headers():
    return {"Accept": "application/json"}


@pytest.fixture(scope="session")
def timeout():
    return 10


@pytest.fixture
def booking_body():
    return {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-05"},
        "additionalneeds": "Breakfast",
    }


@pytest.fixture(scope="function")
def updated_body():
    return {
        "firstname": "Antony",
        "lastname": "Hopkins",
        "totalprice": 121,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-03-03", "checkout": "2026-03-05"},
        "additionalneeds": "Bath",
    }


@pytest.fixture(scope="session")
def credentials():
    password = os.getenv("API_PASSWORD")
    assert password, "API_PASSWORD is not set"
    return {
        "username": "admin",
        "password": password
    }


@pytest.fixture(scope="session")
def auth_token(client, credentials):
    response = client.auth(credentials)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "token" in data, data
    assert isinstance(data["token"], str)
    return data["token"]


@pytest.fixture()
def created_booking(client, booking_body, auth_token):
    created = client.create_booking(booking_body)

    assert created.status_code == 200, created.text
    created_data = created.json()
    assert "bookingid" in created_data, created_data

    booking_id = created_data["bookingid"]
    yield booking_id

    deleted = client.delete_booking(booking_id, auth_token)
    assert deleted.status_code == 201, deleted.text


@pytest.fixture(scope="session")
def client(base_url, headers, timeout):
    client = BookingClient(base_url, headers, timeout)
    return client
