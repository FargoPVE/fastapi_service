from fastapi import APIRouter, Depends
from pydantic import parse_obj_as
from fastapi_cache.decorator import cache

from app.api.celery_tasks import send_booking_confirmation_email
from app.core.dependencies import get_current_user
from app.models.users_model import Users
from app.schemas.booking_schema import SBookingInfo, SNewBooking
from app.services.bookings_service import BookingService
from app.utils.exeptions import RoomCannotBeBooked

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
@cache(expire=30)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingInfo]:
    return await BookingService.find_all_with_images(user_id=user.id)


@router.delete("/{booking_id}")
async def remove_booking(
    booking_id: int,
    current_user: Users = Depends(get_current_user),
):
    await BookingService.delete(id=booking_id, user_id=current_user.id)


@router.post("", status_code=201)
async def create_booking(
    booking: SNewBooking,
    user: Users = Depends(get_current_user),
):
    booking = await BookingService.add(
        user.id, booking.room_id, booking.date_from, booking.date_to
    )
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = parse_obj_as(SNewBooking, booking).model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict
