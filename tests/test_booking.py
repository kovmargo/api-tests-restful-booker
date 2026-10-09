import requests

BASE_URL = "https://restful-booker.herokuapp.com"
HEADERS = {"Accept": "application/json"}
TIMEOUT = 10


def booking_body():
    return {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-05"},
        "additionalneeds": "Breakfast",
    }


def test_create_booking_returns_sent_data():
    body = booking_body()
    response = requests.post(f"{BASE_URL}/booking", json=body, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["booking"]["firstname"] == body["firstname"]
    assert data["booking"]["lastname"] == body["lastname"]
    assert data["booking"]["totalprice"] == body["totalprice"]
    assert isinstance(data["bookingid"], int)


def test_get_bookings_returns_list():
    response = requests.get(
        f"{BASE_URL}/booking",
        headers=HEADERS,
        timeout=TIMEOUT,
    )

    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)


def test_auth_with_valid_credentials_returns_token():
    credentials = {"username": "admin", "password": "password123"}

    response = requests.post(
        f"{BASE_URL}/auth",
        json=credentials, headers=HEADERS, timeout=TIMEOUT
    )

    assert response.status_code == 200, response.text

    data = response.json()
    assert "token" in data, data
    assert isinstance(data["token"], str)
    assert len(data["token"]) > 0  # "token" есть в data
