import requests


def test_create_booking_returns_sent_data(base_url, headers, timeout, booking_body):
    response = requests.post(f"{base_url}/booking", json=booking_body, headers=headers, timeout=timeout)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["booking"]["firstname"] == booking_body["firstname"]
    assert data["booking"]["lastname"] == booking_body["lastname"]
    assert data["booking"]["totalprice"] == booking_body["totalprice"]
    assert isinstance(data["bookingid"], int)


def test_get_bookings_returns_list(base_url, headers, timeout):
    response = requests.get(
        f"{base_url}/booking",
        headers=headers,
        timeout=timeout,
    )

    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)


def test_auth_with_valid_credentials_returns_token(token):
    assert isinstance(token, str)
    assert len(token) > 0


def test_created_booking_can_be_read_back(base_url, headers, timeout, booking_body):
    created = requests.post(f"{base_url}/booking", json=booking_body, headers=headers, timeout=timeout)

    assert created.status_code == 200, created.text
    created_data = created.json()
    assert "bookingid" in created_data, created_data

    booking_id = created_data["bookingid"]

    response = requests.get(
        f"{base_url}/booking/{booking_id}",
        headers=headers,
        timeout=timeout,
    )
    assert response.status_code == 200, response.text
    assert response.json() == booking_body
