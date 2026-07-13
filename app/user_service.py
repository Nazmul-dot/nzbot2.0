from app.dto.user_dto import UserCreateDTO
from app.service.user_service import UserService


def register_user(name: str, email: str, password: str, is_active: bool = True):
    payload = UserCreateDTO(
        name=name,
        email=email,
        password=password,
        is_active=is_active,
    )
    return UserService.register_user(payload)
