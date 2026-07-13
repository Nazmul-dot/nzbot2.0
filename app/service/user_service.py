"""
Service layer = business logic.
Sits between the controller (HTTP concerns) and the DAO (DB concerns).

Rule of thumb:
- Controller: "What did the client ask for?"
- Service:    "What should actually happen?"
- DAO:        "How do I fetch/store that in the DB?"
"""
from secrets import compare_digest

from sqlalchemy.orm import Session

from app.dao.user_dao import UserDAO
from app.dto.user_dto import UserCreateDTO, UserUpdateDTO
from app.schema.user_schema import User
from app.utils.exceptions import AlreadyExistsError, NotFoundError


class UserService:

    def register_user(db: Session, payload: UserCreateDTO) -> User:
        try:
            return UserDAO.create_user(db, payload)
        except ValueError as exc:
            raise AlreadyExistsError(str(exc)) from exc

    def get_user(db: Session, user_id: int) -> User:
        user = UserDAO.get_user_by_id(db, user_id)
        if user is None:
            raise NotFoundError(f"User with ID {user_id} not found.")
        return user

    def update_user(db: Session, user_id: int, payload: UserUpdateDTO) -> User:
        user = UserDAO.get_user_by_id(db, user_id)
        if user is None:
            raise NotFoundError(f"User with ID {user_id} not found.")

        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "email" and value is not None:
                setattr(user, field, str(value).strip().lower())
            elif field == "password" and value is not None:
                setattr(user, field, str(value).strip())
            elif field == "name" and value is not None:
                setattr(user, field, str(value).strip())
            else:
                setattr(user, field, value)

        return UserDAO.update_user(db, user)

    def delete_user(db: Session, user_id: int) -> None:
        user = UserDAO.get_user_by_id(db, user_id)
        if user is None:
            raise NotFoundError(f"User with ID {user_id} not found.")
        UserDAO.delete_user(db, user)

    def list_users(db: Session) -> list[User]:
        return UserDAO.list_users(db)


    def login_user(db: Session, email: str, password: str) -> User:
        user:User = UserDAO.get_user_by_email(db, email)
        if user is None:
            raise NotFoundError("User not found.")
        if not compare_digest(user.password, password):
            raise ValueError("Invalid password.")
        return user
