from fastapi import APIRouter

from app.api.v1.endpoints.auth import auth_router as auth_router, users_router
from app.api.v1.endpoints.bookings import router as bookings_router
from app.api.v1.endpoints.hotels import router as hotels_router
from app.api.v1.endpoints.images import router as images_router
from app.api.v1.endpoints.rooms import router as rooms_router
from app.api.v1.endpoints.importer import router as importer_router

base_router = APIRouter()

base_router.include_router(auth_router)
base_router.include_router(hotels_router)
base_router.include_router(bookings_router)
base_router.include_router(users_router)
base_router.include_router(rooms_router)
base_router.include_router(images_router)
base_router.include_router(importer_router)
