import pytest
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


def test_auth_with_valid_credentials_returns_token(base_url, headers, timeout):
    credentials = {"username": "admin", "password": "password123"}

    response = requests.post(
        f"{base_url}/auth",
        json=credentials, headers=headers, timeout=timeout
    )

    assert response.status_code == 200, response.text

    data = response.json()
    assert "token" in data, data

    assert isinstance(data["token"], str)
    assert len(data["token"]) > 0


def test_create_booking_can_be_read_back(created_booking, base_url, headers, timeout, booking_body):
    booking_id = created_booking

    response = requests.get(
        f"{base_url}/booking/{booking_id}",
        headers=headers,
        timeout=timeout,
    )
    assert response.status_code == 200, response.text
    assert response.json() == booking_body


@pytest.mark.parametrize("username, password", [
    ("", "password123"),
    ("admin", ""),
    ("admin", "password777"),
    ("min", "password123")])
def test_auth_with_invalid_credentials_is_rejected(username, password, base_url, headers, timeout):
    credentials = {"username": username, "password": password}
    response = requests.post(
        f"{base_url}/auth",
        json=credentials, headers=headers, timeout=timeout
    )

    data = response.json()

    assert response.status_code == 200, response.text
    assert "token" not in data, data
    assert data["reason"] == "Bad credentials", data


def test_put_with_token_updates_whole_booking(created_booking, headers, base_url, timeout, token):
    booking_id = created_booking

    put_headers = headers | {"Cookie": f"token={token}"}

    updated_body = {
        "firstname": "Antony",
        "lastname": "Hopkins",
        "totalprice": 121,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-03-03", "checkout": "2026-03-05"},
        "additionalneeds": "Bath",
    }

    response = requests.put(f"{base_url}/booking/{booking_id}", json=updated_body, headers=put_headers, timeout=timeout)

    assert response.status_code == 200, response.text

    get_response = requests.get(f"{base_url}/booking/{booking_id}", headers=headers, timeout=timeout)
    assert get_response.status_code == 200, get_response.text
    assert get_response.json() == updated_body


def test_patch_with_token_changes_only_one_field(created_booking, headers, base_url, timeout, token):
    booking_id = created_booking
    get_before = requests.get(f"{base_url}/booking/{booking_id}", headers=headers, timeout=timeout)
    assert get_before.status_code == 200, get_before.text

    patch_headers = headers | {"Cookie": f"token={token}"}
    updated_firstname = {"firstname": "Malcolm"}
    response = requests.patch(f"{base_url}/booking/{booking_id}", json=updated_firstname, headers=patch_headers,
                              timeout=timeout)
    assert response.status_code == 200, response.text

    get_after = requests.get(f"{base_url}/booking/{booking_id}", headers=headers, timeout=timeout)
    assert get_after.status_code == 200, get_after.text

    expected = get_before.json() | updated_firstname
    assert get_after.json() == expected
