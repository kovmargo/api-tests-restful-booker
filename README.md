# api-tests-restful-booker

[![API tests](https://github.com/kovmargo/api-tests-restful-booker/actions/workflows/tests.yml/badge.svg)](https://github.com/kovmargo/api-tests-restful-booker/actions/workflows/tests.yml)


API tests for [Restful-Booker](https://restful-booker.herokuapp.com), a public demo API for hotel bookings.
Written in Python with pytest and requests.
Tests talk to the API through a small API client class, `BookingClient`, not through raw `requests` calls.

## What is tested

- `POST /auth`: valid and invalid login
- `GET /booking` and `GET /booking/{id}`: list, read back, unknown id → 404
- `POST /booking`: create, missing fields, wrong data types
- `PUT`, `PATCH`, `DELETE /booking/{id}`: with token, and `PUT` without token

## Requirements

- Python 3.10+
- Internet access (tests call the live API)

## Installation

```bash
git clone <repo-url>
cd api-tests-restful-booker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the tests

First set the API password (the default admin password from the Restful-Booker docs):

```bash
export API_PASSWORD=<password>
```

All tests:

```bash
pytest -v
```

One test by name:

```bash
pytest -v -k test_get_bookings_returns_list
```

Choose the environment with `--env` (default is `prod`):

```bash
pytest -v --env prod    # https://restful-booker.herokuapp.com
pytest -v --env local   # http://localhost:3001 (Restful-Booker running in Docker)
```

pytest settings (test folder, markers, strict xfail) are in `pytest.ini`.

## Project structure

```
api/
  booking_client.py # BookingClient: one method per endpoint (get, create, auth, put, patch, delete)
tests/
  conftest.py       # shared fixtures: --env option, client, credentials, auth_token, created_booking, booking data
  test_booking.py   # the tests (use the client fixture)
BUGS.md             # bugs found in the API
explore.py          # small script to explore the API by hand
pytest.ini          # pytest settings: testpaths, markers, xfail_strict
requirements.txt    # dependencies
```

## How the tests are organised

```
test  →  client fixture  →  BookingClient  →  Restful-Booker API
```

- `BookingClient` keeps `base_url`, headers and timeout, and has one method per endpoint.
- Methods return the full response. All checks (`assert`) stay in the tests.
- `put_booking`, `patch_booking` and `delete_booking` take an optional `token`. Without it, no auth cookie is sent (used by negative tests).
- If the API changes (path, headers, how the token is sent), only `api/booking_client.py` needs to change.

## Known bugs (xfailed tests)

Some tests are marked `xfail`: they check the **correct** behaviour, but the API has a bug, so they fail on purpose.
A normal run looks like this:

```
13 passed, 6 xfailed
```

`xfailed` is expected and not a problem. Details for each bug: [BUGS.md](BUGS.md).
