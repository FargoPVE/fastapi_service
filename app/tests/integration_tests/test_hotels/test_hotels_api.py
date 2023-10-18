import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "location,date_from,date_to,status_code,detail",
    [
        (
            "Алтай",
            "2023-01-01",
            "2022-01-10",
            400,
            "The arrival date cannot be later than the departure date.",
        ),
        (
            "Алтай",
            "2023-01-01",
            "2023-02-10",
            400,
            "It is not possible to book a hotel for more than a month.",
        ),
        ("Алтай", "2023-01-01", "2023-01-10", 200, None),
    ],
)
async def test_get_hotels_by_location_and_time(
    location,
    date_from,
    date_to,
    status_code,
    detail,
    ac: AsyncClient,
):
    response = await ac.get(
        f"/api/v1/hotels/{location}",
        params={
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code
    if str(status_code).startswith("4"):
        assert response.json()["detail"] == detail
