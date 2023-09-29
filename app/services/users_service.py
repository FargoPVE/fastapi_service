from app.models.users_model import Users
from app.services.base_service import BaseService


class UserService(BaseService):
    model = Users
