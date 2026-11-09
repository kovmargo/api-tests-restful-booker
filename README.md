# api-tests-restful-booker

[![API tests](https://github.com/kovmargo/api-tests-restful-booker/actions/workflows/tests.yml/badge.svg)](https://github.com/kovmargo/api-tests-restful-booker/actions/workflows/tests.yml)


API tests for [Restful-Booker](https://restful-booker.herokuapp.com), a public demo API for hotel bookings.
Written in Python with pytest and requests.

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
tests/
  conftest.py       # shared fixtures: base_url, headers, auth_token, auth_headers, booking data
  test_booking.py   # the tests
BUGS.md             # bugs found in the API
explore.py          # small script to explore the API by hand
pytest.ini          # pytest settings: testpaths, markers, xfail_strict
requirements.txt    # dependencies
```

## Known bugs (xfailed tests)

Some tests are marked `xfail`: they check the **correct** behaviour, but the API has a bug, so they fail on purpose.
A normal run looks like this:

```
13 passed, 6 xfailed
```

`xfailed` is expected and not a problem. Details for each bug: [BUGS.md](BUGS.md).
