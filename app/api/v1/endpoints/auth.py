from fastapi import APIRouter, Depends, Response

from app.core.auth import authenticate_user, create_access_token, get_password_hash
from app.core.dependencies import get_current_user
from app.models.users_model import Users
from app.schemas.user_schema import SUserAuth
from app.services.users_service import UserService
from app.utils.exeptions import (
    UnauthorizedException,
    UserAlreadyExistsException,
    CannotAddDataToDatabase,
)

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentification"]
)

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@auth_router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    new_user = await UserService.add(email=user_data.email, hashed_password=hashed_password)
    if not new_user:
        raise CannotAddDataToDatabase


@auth_router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}

@auth_router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")

@users_router.get("/me")
async def get_current_user(current_user: Users = Depends(get_current_user)):
    if not current_user:
        raise UnauthorizedException
    return current_user

@users_router.get("/all")
async def get_all_users(current_user: Users = Depends(get_current_user)):
    if not current_user:
        raise UnauthorizedException
    return await UserService.find_all()