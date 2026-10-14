# Bugs found in Restful-Booker

## BUG-1: POST /auth with wrong password returns 200
Steps: POST /auth {"username": "admin", "password": "wrong"}
Expected: 401 Unauthorized
Actual: 200 OK, body {"reason": "Bad credentials"}
Test: test_auth_with_invalid_credentials_is_rejected

## BUG-2: POST /booking without one required field returns 500
Steps: POST /booking with a valid body, but remove ONE required field
       (tried each: firstname, lastname, totalprice, depositpaid, bookingdates)
Expected: 400 Bad Request with a message about the missing field
Actual: 500, body "Internal Server Error" (same for all 5 fields)
Test: test_post_booking_with_missing_field

## BUG-3: PUT /booking/{id} without token returns 403
Steps: PUT /booking/{id} with a valid body and no Cookie / Authorization header
Expected: 401 Unauthorized (client is not authenticated)
Actual: 403 Forbidden (data is not changed, which is correct)
Test: test_put_without_token_is_rejected

## BUG-4: DELETE /booking/{id} returns 201
Steps: DELETE /booking/{id} with a valid token
Expected: 200 OK or 204 No Content
Actual: 201 Created (booking is really deleted, GET returns 404)
Test: test_delete_with_token_removes_booking

## BUG-5: POST /booking with text in totalprice returns 200 and saves null
Steps: POST /booking with a valid body, but "totalprice": "test price"
Expected: 400 Bad Request (totalprice must be a number)
Actual: 200 OK, booking is created with "totalprice": null (the price is silently lost)
Test: test_post_booking_with_string_totalprice
