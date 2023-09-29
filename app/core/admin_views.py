from sqladmin import ModelView

from app.models.bookings_model import Bookings
from app.models.hotels_model import Hotels
from app.models.rooms_model import Rooms
from app.models.users_model import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    can_delete = False
    column_details_exclude_list = [Users.hashed_password]
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    category = "accounts"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]
    name = "Hotel"
    name_plural = "Hotels"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.booking]
    name = "Room"
    name_plural = "Rooms"
    icon = "fa-solid fa-bed"


class BookingAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user]
    name = "Booking"
    name_plural = "Bookings"
    icon = "fa-solid fa-book"