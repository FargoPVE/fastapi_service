from datetime import date, datetime, timedelta
from typing import List

from fastapi import Query
from fastapi_cache.decorator import cache

from app.api.v1.endpoints.hotels import router
from app.schemas.rooms_schema import SRoomInfo
from app.services.rooms_services import RoomService


@router.get("/{hotel_id}/rooms")
@cache(expire=30)
async def get_rooms_by_time(
    hotel_id: str,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(
        ..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"
    ),
) -> List[SRoomInfo]:
    rooms = await RoomService.find_all(hotel_id, date_from, date_to)
    return rooms
