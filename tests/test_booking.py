import pytest
from api.models import CreateBookingResponse
from api.models import Booking


def test_create_booking_returns_sent_data(client, booking_body):
    response = client.create_booking(booking_body)
    assert response.status_code == 200, response.text

    data = response.json()
    created = CreateBookingResponse.model_validate(data)
    assert created.booking.model_dump() == booking_body


@pytest.mark.smoke
def test_get_bookings_returns_list(client):
    response = client.get_bookings()

    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)


@pytest.mark.smoke
def test_auth_with_valid_credentials_returns_token(credentials, client):
    response = client.auth(credentials)

    assert response.status_code == 200, response.text

    data = response.json()
    assert "token" in data, data

    assert isinstance(data["token"], str)
    assert len(data["token"]) > 0


@pytest.mark.smoke
def test_create_booking_can_be_read_back(created_booking, booking_body, client):
    booking_id = created_booking
    response = client.get_booking(booking_id)
    assert response.status_code == 200, response.text

    read_back = Booking.model_validate(response.json())
    assert read_back.model_dump() == booking_body


@pytest.mark.parametrize("field, value", [
    ("username", ""),
    ("password", ""),
    ("password", "password777"),
    ("username", "min")])
def test_auth_with_invalid_credentials_is_rejected(field, value, credentials, client):
    bad_credentials = credentials | {field: value}
    response = client.auth(bad_credentials)

    assert response.status_code == 200, response.text

    data = response.json()
    assert "token" not in data, data
    assert data["reason"] == "Bad credentials", data


def test_put_with_token_updates_whole_booking(auth_token, created_booking, updated_body, client):
    booking_id = created_booking

    response = client.put_booking(booking_id, updated_body, auth_token)
    assert response.status_code == 200, response.text

    get_response = client.get_booking(booking_id)

    assert get_response.status_code == 200, get_response.text
    assert get_response.json() == updated_body


def test_patch_with_token_changes_only_one_field(created_booking, client, auth_token):
    booking_id = created_booking
    get_before = client.get_booking(booking_id)
    assert get_before.status_code == 200, get_before.text

    updated_firstname = {"firstname": "Malcolm"}
    response = client.patch_booking(booking_id, updated_firstname, auth_token)
    assert response.status_code == 200, response.text

    get_after = client.get_booking(booking_id)
    assert get_after.status_code == 200, get_after.text

    expected = get_before.json() | updated_firstname
    assert get_after.json() == expected


def test_delete_with_token_removes_booking(booking_body, client, auth_token):
    new_booking = client.create_booking(booking_body)
    assert new_booking.status_code == 200, new_booking.text
    booking_id = new_booking.json()["bookingid"]

    delete_response = client.delete_booking(booking_id, auth_token)
    assert delete_response.status_code == 201, delete_response.text

    get_booking = client.get_booking(booking_id)
    assert get_booking.status_code == 404, get_booking.text


def test_put_without_token_is_rejected(created_booking, updated_body, client):
    booking_id = created_booking
    before_response = client.get_booking(booking_id)
    assert before_response.status_code == 200, before_response.text

    response = client.put_booking(booking_id, updated_body)
    assert response.status_code == 403, response.text

    after_response = client.get_booking(booking_id)
    assert after_response.status_code == 200, after_response.text
    assert after_response.json() == before_response.json()

@pytest.mark.parametrize("wrong_token", ["sdfdfsdf123578sdffsd", "", "null"],
                         ids=["random", "empty", "null"])
def test_put_with_wrong_token_is_forbidden(created_booking, updated_body, client, booking_body, wrong_token):
    booking_id = created_booking

    put_response = client.put_booking(booking_id, updated_body, token=wrong_token)
    assert put_response.status_code == 403, put_response.text

    get_response = client.get_booking(booking_id)
    assert get_response.status_code == 200, get_response.text

    read_back = Booking.model_validate(get_response.json())
    assert read_back.model_dump() == booking_body


def test_get_booking_with_unknown_id_returns_404(client):
    booking_id = 0
    response = client.get_booking(booking_id)

    assert response.status_code == 404, response.text


@pytest.mark.parametrize("missing_field", [
    ("firstname"),
    ("lastname"),
    ("totalprice"),
    ("depositpaid"),
    ("bookingdates")])
@pytest.mark.xfail(reason="BUG-2: returns 500 instead of 400", strict=True)
def test_post_booking_with_missing_field(booking_body, missing_field, client):
    copy_booking_body = booking_body.copy()
    copy_booking_body.pop(missing_field)

    response = client.create_booking(copy_booking_body)

    assert response.status_code == 400, response.text


@pytest.mark.xfail(reason="BUG-5: accepts text in totalprice, saves null", strict=True)
def test_post_booking_with_string_totalprice(booking_body, client):
    booking_body["totalprice"] = "test price"

    response = client.create_booking(booking_body)

    assert response.status_code == 400, response.text
