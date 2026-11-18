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

    def create_booking(self, body):
        return requests.post(f"{self.base_url}/booking", json=body, headers=self.headers,
                             timeout=self.timeout)

    def auth(self, credentials):
        return requests.post(
            f"{self.base_url}/auth", json=credentials, headers=self.headers,
            timeout=self.timeout)

    def put_booking(self, booking_id, body, token=None):
        headers = self._build_headers(token)
        return requests.put(f"{self.base_url}/booking/{booking_id}", json=body,
                            headers=headers, timeout=self.timeout)

    def patch_booking(self, booking_id, body, token=None):
        headers = self._build_headers(token)
        return requests.patch(f"{self.base_url}/booking/{booking_id}", json=body,
                              headers=headers, timeout=self.timeout)

    def delete_booking(self, booking_id, token=None):
        headers = self._build_headers(token)
        return requests.delete(f"{self.base_url}/booking/{booking_id}", headers=headers,
                               timeout=self.timeout)

    def _build_headers(self, token=None):
        if token is None:
            return self.headers
        else:
            return self.headers | {"Cookie": f"token={token}"}
