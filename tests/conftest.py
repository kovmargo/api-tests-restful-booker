import pytest
import requests


@pytest.fixture(scope="session")
def base_url():
    return "https://restful-booker.herokuapp.com"


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


@pytest.fixture()
def token(base_url, headers, timeout):
    credentials = {"username": "admin", "password": "password123"}

    response = requests.post(
        f"{base_url}/auth",
        json=credentials, headers=headers, timeout=timeout
    )

    data = response.json()
    assert "token" in data, data
    assert isinstance(data["token"], str)
    return data["token"]

