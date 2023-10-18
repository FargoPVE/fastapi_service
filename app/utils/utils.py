from datetime import datetime, timedelta
import json
from typing import Iterable

from app.services.rooms_services import RoomService
from app.services.hotels_service import HotelService
from app.services.bookings_service import BookingService
from app.utils.logger import logger

TABLE_MODEL_MAP = {
    "hotels": HotelService,
    "rooms": RoomService,
    "bookings": BookingService,
}


def convert_csv_to_postgres_format(csv_iterable: Iterable):
    try:
        data = []
        for row in csv_iterable:
            for k, v in row.items():
                if v.isdigit():
                    row[k] = int(v)
                elif k == "services":
                    row[k] = json.loads(v.replace("'", '"'))
                elif "date" in k:
                    row[k] = datetime.strptime(v, "%Y-%m-%d")
            data.append(row)
        return data
    except Exception:
        logger.error("Cannot convert CSV into DB format", exc_info=True)


def get_month_days(date: datetime = datetime.today()):
    counter = datetime(date.year, date.month, datetime.today().day, tzinfo=date.tzinfo)
    date_list = []
    for _ in range(365 * 2):
        date_list.append(
            {"date": counter.date(), "date_formatted": counter.strftime("%Y-%m-%d")}
        )
        counter += timedelta(days=1)
    return date_list


def format_number_thousand_separator(
    number: int,
    separator: str = " ",
):
    return f"{number:,}".replace(",", separator)
