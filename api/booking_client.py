import requests

class BookingClient(object):

    def __init__(self, base_url, headers, timeout):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    def get_bookings(self):
        return requests.get(f"{self.base_url}/booking", headers=self.headers,
                            timeout=self.timeout)

    def get_booking(self, booking_id):
        return requests.get(f"{self.base_url}/booking/{booking_id}", headers=self.headers,
                            timeout=self.timeout)
