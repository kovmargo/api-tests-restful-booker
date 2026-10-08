"""Explore the Restful Booker API: list booking ids and show one booking."""
import requests

BASE_URL = "https://restful-booker.herokuapp.com"


def get_booking_ids():
    """Return a list of all booking ids from GET /booking."""
    response = requests.get(f"{BASE_URL}/booking", timeout=10)

    response.raise_for_status()
    bookings = response.json()

    booking_ids = []
    for x in bookings:
        booking_ids.append(x['bookingid'])

    return booking_ids


def get_booking(booking_id):
    """Return booking data as a dict from GET /booking/{booking_id}.

    Raises requests.HTTPError if the booking is not found (404).
    """
    response = requests.get(
        f"{BASE_URL}/booking/{booking_id}",
        headers={"Accept": "application/json"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def main():
    """Print all booking ids and details of the first booking."""
    ids = get_booking_ids()
    if not ids:
        print("Empty list of bookings")
        return

    for booking_id in ids:
        print(booking_id)

    booking = get_booking(ids[0])
    print(
        f"Booking {ids[0]}: firstname = {booking['firstname']}, "
        f"totalprice = {booking['totalprice']}, "
        f"checkin = {booking['bookingdates']['checkin']}"
    )


if __name__ == "__main__":
    main()
