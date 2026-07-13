"""
Controller = the layer that talks HTTP.

It receives the request (already validated into a DTO by FastAPI),
calls the service layer to do the actual work, and translates any
errors/results into proper HTTP responses.

It should contain NO business logic and NO direct DB queries.
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.dto.user_dto import TokenResponseDTO, UserCreateDTO, UserResponseDTO, UserUpdateDTO
from app.service.user_service import UserService
from app.utils.exceptions import AlreadyExistsError, NotFoundError


def create_user(db: Session, payload: UserCreateDTO):
    try:
        user = UserService.register_user(db, payload)
        return UserResponseDTO.model_validate(user)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except AlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


def get_user(db: Session, user_id: int):
    try:
        user = UserService.get_user(db, user_id)
        return UserResponseDTO.model_validate(user)
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


def update_user(db: Session, user_id: int, payload: UserUpdateDTO):
    try:
        user = UserService.update_user(db, user_id, payload)
        return UserResponseDTO.model_validate(user)
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


def delete_user(db: Session, user_id: int):
    try:
        UserService.delete_user(db, user_id)
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


def list_users(db: Session):
    users = UserService.list_users(db)
    return [UserResponseDTO.model_validate(user) for user in users]


def login_user(db: Session, email: str, password: str):
    try:
        user: User = UserService.login_user(db, email, password)
        return TokenResponseDTO(
            access_token=create_access_token(user.id, user.email),
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponseDTO.model_validate(user),
        )
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
