# api-tests-restful-booker

[![API tests](https://github.com/kovmargo/api-tests-restful-booker/actions/workflows/tests.yml/badge.svg)](https://github.com/kovmargo/api-tests-restful-booker/actions/workflows/tests.yml)

API test framework for [Restful-Booker](https://restful-booker.herokuapp.com), a public demo API for hotel bookings.

**Stack:** Python · pytest · requests · pydantic · Faker · GitHub Actions

## Highlights

- Typed API client, `BookingClient`: tests never call `requests` directly
  (see [How the tests are organised](#how-the-tests-are-organised)).
- Response schema validation with Pydantic (strict mode).
- Fresh test data generated with Faker, with setup and cleanup handled by pytest fixtures where applicable.
- Parallel test execution with pytest-xdist.
- Automated test runs with GitHub Actions and HTML reporting.
- **7 API issues found and documented** (see [Bugs found](#bugs-found)).

## What is tested

- `POST /auth`: valid credentials return a token; an empty or incorrect username or password is rejected with a
  `"Bad credentials"` message and no token
- `GET /booking`, `GET /booking/{id}`: checks that the booking list is returned, validates the schema and data of a
  created booking, and checks for 404 when the id is unknown
- `POST /booking`: checks the response schema and verifies that the returned data matches the request; expects 400 for
  missing required fields, a string in `totalprice`, and checkout before checkin (known issues, marked as `xfail`)
- `PUT`, `PATCH`, `DELETE /booking/{id}`:
    - with a valid token: full update, partial update, delete
    - with a missing or invalid token (random, empty, `"null"`) → 403, and the booking stays unchanged
    - with an unknown id → expects 404 (marked as `xfail`)

## Bugs found

A normal run looks like this:

```
24 passed, 10 xfailed
```

`xfailed` tests check the **correct** behaviour and fail on purpose, because the API has a bug. `strict=True` means that
if a bug gets fixed, the test turns red, so the marker can be removed.

Some of the bugs:

- **BUG-6:** `PUT`/`PATCH`/`DELETE` on a booking that does not exist return `405 Method Not Allowed` instead of
  `404 Not Found`
- **BUG-7:** a booking with checkout **before** checkin is accepted (`200`) and saved
- **BUG-5:** text in `totalprice` is accepted (`200`) and the price is silently saved as `null`
- **BUG-2:** a request with one required field missing crashes the server (`500`) instead of returning `400`

Full list with steps, expected and actual results: [BUGS.md](BUGS.md).

## Requirements

- Python 3.10+
- Internet access (tests call the live API)

## Installation

```bash
git clone https://github.com/kovmargo/api-tests-restful-booker.git
cd api-tests-restful-booker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the tests

Set the API password first. It is the public demo password from the Restful-Booker docs, and it is never stored in the
code:

```bash
export API_PASSWORD=password123
```

All tests:

```bash
pytest -v
```

Only the quick smoke checks:

```bash
pytest -v -m smoke
```

One test by name:

```bash
pytest -v -k test_get_bookings_returns_list
```

In parallel:

```bash
pytest -v -n 4
```

Choose the environment with `--env` (default is `prod`):

```bash
pytest -v --env prod    # https://restful-booker.herokuapp.com
pytest -v --env local   # http://localhost:3001 (Restful-Booker running in Docker)
```

pytest settings (test folder, markers, strict xfail) are in `pytest.ini`.

## CI

GitHub Actions (`.github/workflows/tests.yml`) runs the tests:

- on every push and pull request to `main`
- every night (scheduled run), to catch changes on the live API
- by hand, with a choice of all tests or smoke tests only

Tests run in parallel, and the HTML report is uploaded as a build artifact. The password comes from GitHub Secrets.

## Project structure

```
api/
  booking_client.py # BookingClient: one method per endpoint (get, create, auth, put, patch, delete)
  models.py         # Booking, BookingDates, CreateBookingResponse models
tests/
  conftest.py       # fixtures: --env option, client, credentials, auth_token, created_booking, booking data
  test_booking.py   # the tests
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
- `put_booking`, `patch_booking` and `delete_booking` take an optional `token`. Without it, no auth cookie is sent (used
  by negative tests).
- If the API changes (path, headers, how the token is sent), only `api/booking_client.py` needs to change.
- Each test checks in the same order: status code → response shape (pydantic model) → values.
