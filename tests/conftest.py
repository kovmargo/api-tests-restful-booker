import os
from datetime import timedelta

import pytest
from faker import Faker

from api.booking_client import BookingClient

fake = Faker()


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


def random_booking_dates():
    checkin = fake.date_between(start_date="+1d", end_date="+30d")
    checkout = checkin + timedelta(days=fake.random_int(min=1, max=7))
    return {"checkin": checkin.isoformat(), "checkout": checkout.isoformat()}


@pytest.fixture
def booking_body():
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=50, max=500),
        "depositpaid": fake.boolean(),
        "bookingdates": random_booking_dates(),
        "additionalneeds": fake.random_element(["Breakfast", "Lunch", "Dinner"]),
    }


@pytest.fixture(scope="function")
def updated_body():
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=50, max=500),
        "depositpaid": fake.boolean(),
        "bookingdates": random_booking_dates(),
        "additionalneeds": fake.random_element(["Bath", "Late checkout", "Parking"]),
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
