from pydantic import BaseModel, ConfigDict


class BookingDates(BaseModel):
    model_config = ConfigDict(strict=True)
    checkin: str
    checkout: str


class Booking(BaseModel):
    model_config = ConfigDict(strict=True)
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str


class CreateBookingResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    bookingid: int
    booking: Booking
