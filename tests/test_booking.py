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

@pytest.mark.smoke
def test_get_bookings_returns_list(base_url, headers, timeout):
    response = requests.get(
        f"{base_url}/booking",
        headers=headers,
        timeout=timeout,
    )

    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)

@pytest.mark.smoke
def test_auth_with_valid_credentials_returns_token(base_url, headers, timeout, credentials):
    response = requests.post(
        f"{base_url}/auth",
        json=credentials, headers=headers, timeout=timeout
    )

    assert response.status_code == 200, response.text

    data = response.json()
    assert "token" in data, data

    assert isinstance(data["token"], str)
    assert len(data["token"]) > 0


@pytest.mark.smoke
def test_create_booking_can_be_read_back(created_booking, base_url, headers, timeout, booking_body):
    booking_id = created_booking

    response = requests.get(
        f"{base_url}/booking/{booking_id}",
        headers=headers,
        timeout=timeout,
    )
    assert response.status_code == 200, response.text
    assert response.json() == booking_body


@pytest.mark.parametrize("field, value", [
    ("username", ""),
    ("password", ""),
    ("password", "password777"),
    ("username", "min")])
def test_auth_with_invalid_credentials_is_rejected(field, value, credentials, base_url, headers, timeout):
    bad_credentials = credentials | {field: value}
    response = requests.post(
        f"{base_url}/auth",
        json=bad_credentials, headers=headers, timeout=timeout
    )
    assert response.status_code == 200, response.text

    data = response.json()
    assert "token" not in data, data
    assert data["reason"] == "Bad credentials", data

def test_put_with_token_updates_whole_booking(auth_headers, created_booking, headers, base_url, timeout, updated_body):
    booking_id = created_booking

    response = requests.put(f"{base_url}/booking/{booking_id}", json=updated_body, headers=auth_headers, timeout=timeout)
    assert response.status_code == 200, response.text

    get_response = requests.get(f"{base_url}/booking/{booking_id}", headers=headers, timeout=timeout)
    assert get_response.status_code == 200, get_response.text
    assert get_response.json() == updated_body


def test_patch_with_token_changes_only_one_field(created_booking, headers, base_url, timeout, auth_headers):
    booking_id = created_booking
    get_before = requests.get(f"{base_url}/booking/{booking_id}", headers=headers, timeout=timeout)
    assert get_before.status_code == 200, get_before.text


    updated_firstname = {"firstname": "Malcolm"}
    response = requests.patch(f"{base_url}/booking/{booking_id}", json=updated_firstname, headers=auth_headers,
                              timeout=timeout)
    assert response.status_code == 200, response.text

    get_after = requests.get(f"{base_url}/booking/{booking_id}", headers=headers, timeout=timeout)
    assert get_after.status_code == 200, get_after.text

    expected = get_before.json() | updated_firstname
    assert get_after.json() == expected


def test_delete_with_token_removes_booking(booking_body, base_url, headers, timeout, auth_headers):
    new_booking = requests.post(f"{base_url}/booking", json=booking_body, headers=headers, timeout=timeout)
    assert new_booking.status_code == 200, new_booking.text
    booking_id = new_booking.json()["bookingid"]

    delete_response = requests.delete(f"{base_url}/booking/{booking_id}", headers=auth_headers,
                                      timeout=timeout)
    assert delete_response.status_code == 201, delete_response.text

    get_booking = requests.get(f"{base_url}/booking/{booking_id}", headers=headers, timeout=timeout)
    assert get_booking.status_code == 404, get_booking.text


def test_put_without_token_is_rejected(base_url, created_booking, headers, timeout, updated_body):
    booking_id = created_booking
    before_response = requests.get(f"{base_url}/booking/{booking_id}", headers=headers, timeout=timeout)
    assert before_response.status_code == 200, before_response.text

    response = requests.put(f"{base_url}/booking/{booking_id}", json=updated_body, headers=headers, timeout=timeout)
    assert response.status_code == 403, response.text

    after_response = requests.get(f"{base_url}/booking/{booking_id}", headers=headers, timeout=timeout)
    assert after_response.status_code == 200, after_response.text
    assert after_response.json() == before_response.json()


def test_get_booking_with_unknown_id_returns_404(base_url, headers, timeout):
    booking_id = 0

    response = requests.get(
        f"{base_url}/booking/{booking_id}",
        headers=headers,
        timeout=timeout,
    )
    assert response.status_code == 404, response.text



@pytest.mark.parametrize("missing_field", [
    ("firstname"),
    ("lastname"),
    ("totalprice"),
    ("depositpaid"),
     ("bookingdates")])
@pytest.mark.xfail(reason="BUG-2: returns 500 instead of 400", strict=True)
def test_post_booking_with_missing_field(base_url, headers, timeout, booking_body, missing_field):
    copy_booking_body = booking_body.copy()
    copy_booking_body.pop(missing_field)

    response = requests.post(f"{base_url}/booking", json=copy_booking_body, headers=headers, timeout=timeout)
    assert response.status_code == 400, response.text


@pytest.mark.xfail(reason="BUG-5: accepts text in totalprice, saves null", strict=True)
def test_post_booking_with_string_totalprice(base_url, headers, timeout, booking_body):
    booking_body["totalprice"] = "test price"
    response = requests.post(f"{base_url}/booking", json=booking_body, headers=headers, timeout=timeout)
    assert response.status_code == 400, response.text




