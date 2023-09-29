from typing import Any, Dict

from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code: int = 500
    detail: Any = ""
    headers: Dict[str, str] | None = None
    
    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail, headers=self.headers)

class UserAlreadyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="User already exists."


class IncorrectEmailOrPasswordException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Incorrect email or password."


class UnauthorizedException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Unauthorized user."


class TokenExpiredException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Token expired."


class TokenAbsentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Token is missing."


class IncorrectTokenFormatException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Incorrect token format."


class UserIsNotPresentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Incorrect token format."


class RoomCannotBeBooked(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Room can't be booked."


class RoomFullyBooked(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="There are no available rooms left."


class DateFromCannotBeAfterDateTo(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="The arrival date cannot be later than the departure date."


class CannotBookHotelForLongPeriod(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="It is not possible to book a hotel for more than a month."


class CannotAddDataToDatabase(BookingException):
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Failed to add entry."


class CannotProcessCSV(BookingException):
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Failed to process CSV file."