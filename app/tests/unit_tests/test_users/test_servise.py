import pytest

from app.services.users_service import UserService


@pytest.mark.parametrize("user_id, email, exists", [
    (1, "alex@mail.ru", True),
    (2, "gena@google.com", True),
    (3, "pupa@yandex.ru", True),
    (6, "...", False),
    (7, "...", False),
])
async def test_find_user_by_id(user_id: int, email: str, exists: bool):
    user = await UserService.find_by_id(user_id)

    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user


@pytest.mark.parametrize("user_id, email, hashed_password, exists", [
    (1, "alex@mail.ru", "$2b$12$cu8nV9BRwC3oX6EaaxVbIuirsUG6nudwEp4n6h/XMvDvEFkOBhlOq", True),
    (2, "gena@google.com", "$2b$12$cu8nV9BRwC3oX6EaaxVbIuirsUG6nudwEp4n6h/XMvDvEFkOBhlOq", True),
    (3, "pupa@yandex.ru", "$2b$12$cu8nV9BRwC3oX6EaaxVbIuirsUG6nudwEp4n6h/XMvDvEFkOBhlOq", True),
])
async def test_find_all_users(user_id: int, email: str, hashed_password:str, exists: bool):
    users = await UserService.find_all()

    if exists:
        assert users
        assert users[user_id - 1].id == user_id
        assert users[user_id - 1].email == email
        assert users[user_id - 1].hashed_password == hashed_password
    else:
        assert not users


@pytest.mark.parametrize("user_id, email, hashed_password, exists", [
    (1, "alex@mail.ru", "$2b$12$cu8nV9BRwC3oX6EaaxVbIuirsUG6nudwEp4n6h/XMvDvEFkOBhlOq", True),
    (2, "gena@google.com", "$2b$12$cu8nV9BRwC3oX6EaaxVbIuirsUG6nudwEp4n6h/XMvDvEFkOBhlOq", True),
    (3, "pupa@yandex.ru", "$2b$12$cu8nV9BRwC3oX6EaaxVbIuirsUG6nudwEp4n6h/XMvDvEFkOBhlOq", True),
    (6, "guru@mail.ru", "...", False),
    (7, "upa@dance.com", "...", False),
])
async def test_find_one_or_none_users(user_id: int, email: str, hashed_password:str, exists: bool):
    user = await UserService.find_one_or_none(email=email)

    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
        assert user.hashed_password == hashed_password
    else:
        assert not user