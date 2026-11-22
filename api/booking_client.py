import requests
from requests import Response


class BookingClient():

    def __init__(self, base_url: str, headers: dict, timeout: int) -> None:
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    def get_bookings(self) -> Response:
        return requests.get(f"{self.base_url}/booking", headers=self.headers,
                            timeout=self.timeout)

    def get_booking(self, booking_id: int) -> Response:
        return requests.get(f"{self.base_url}/booking/{booking_id}", headers=self.headers,
                            timeout=self.timeout)

    def create_booking(self, body: dict) -> Response:
        return requests.post(f"{self.base_url}/booking", json=body, headers=self.headers,
                             timeout=self.timeout)

    def auth(self, credentials: dict) -> Response:
        return requests.post(
            f"{self.base_url}/auth", json=credentials, headers=self.headers,
            timeout=self.timeout)

    def put_booking(self, booking_id: int, body: dict, token: str | None = None) -> Response:
        headers = self._build_headers(token)
        return requests.put(f"{self.base_url}/booking/{booking_id}", json=body,
                            headers=headers, timeout=self.timeout)

    def patch_booking(self, booking_id: int, body: dict, token: str | None = None) -> Response:
        headers = self._build_headers(token)
        return requests.patch(f"{self.base_url}/booking/{booking_id}", json=body,
                              headers=headers, timeout=self.timeout)

    def delete_booking(self, booking_id: int, token: str | None = None) -> Response:
        headers = self._build_headers(token)
        return requests.delete(f"{self.base_url}/booking/{booking_id}", headers=headers,
                               timeout=self.timeout)

    def _build_headers(self, token: str | None = None) -> dict:
        if token is None:
            return self.headers
        else:
            return self.headers | {"Cookie": f"token={token}"}
