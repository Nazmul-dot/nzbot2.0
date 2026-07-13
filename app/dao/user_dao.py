"""
DAO (Data Access Object) = ONLY talks to the database.
No business logic here — just CRUD queries against the User table.
Services call these functions; these functions never call services.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dto.user_dto import UserCreateDTO
from app.schema.user_schema import User


class UserDAO:


    def create_user(db: Session, payload: UserCreateDTO) -> User:
        normalized_email = str(payload.email).strip().lower()
        existing_user = db.scalar(select(User).where(User.email == normalized_email))

        if existing_user is not None:
            raise ValueError("A user with this email already exists.")

        user = User(
            name=str(payload.name).strip(),
            email=normalized_email,
            password=str(payload.password).strip(),
            is_active=payload.is_active,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    
    def update_user(db: Session, user: User) -> User:
        db.commit()
        db.refresh(user)
        return user

    
    def delete_user(db: Session, user: User) -> None:
        db.delete(user)
        db.commit()

    
    def list_users(db: Session) -> list[User]:
        # return db.scalars(select(User).order_by(User.id)).all()
        return db.query(User).order_by(User.id).all()

    
    def get_user_by_email(db: Session, email: str) -> User | None:
        normalized_email = str(email).strip().lower()
        return db.query(User).filter(User.email == normalized_email).first()
