import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email, password, status_code", [
    ("alesha@mail.ru", "alesha", 200),
    ("alesha@mail.ru", "aleshAss", 409),
    ("dimas@gmail.com", "DimaDimaAyAyAy", 200),
    ("KlickKlack", "FreeMail", 422),
])
async def test_register_user(email: str, password: str, status_code: int, ac: AsyncClient):
    response = await ac.post("/api/v1/auth/register", json={
        "email": email,
        "password": password
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("email, password, status_code", [
    ("alex@mail.ru", "test", 200),
    ("gena@google.com", "test", 200),
    ("pupa@yandex.ru", "test", 200),
    ("whoiam@mail.ru", "test", 401),
])
async def test_login_user(email: str, password: str, status_code: int, ac: AsyncClient):
    response = await ac.post("/api/v1/auth/login", json={
        "email": email,
        "password": password
    })
    assert response.status_code == status_code
