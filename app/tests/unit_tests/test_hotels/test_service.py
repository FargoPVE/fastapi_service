import pytest

from app.services.hotels_service import HotelService


@pytest.mark.parametrize("hotel_id, is_present", [
    (1, True),
    (2, True),
    (7, False),
])
async def test_find_user_by_id(hotel_id, is_present):
    hotel = await HotelService.find_one_or_none(id=hotel_id)

    if is_present:
        assert hotel
        assert hotel["id"] == hotel_id
    else:
        assert not hotel