"""
Router = maps URL + HTTP method → controller function.
This is the ONLY file that should have @router.get/post/etc decorators.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dto.user_dto import LoginDTO, UserCreateDTO, UserUpdateDTO, UserResponseDTO
from app.controllers import user_controller

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/health", status_code=200)
def health_check():
    return {"status": "healthy"}

@router.post("/", response_model=UserResponseDTO, status_code=201)
def create_user(payload: UserCreateDTO, db: Session = Depends(get_db)):
    return user_controller.create_user(db, payload)

@router.post("/login", response_model=UserResponseDTO)
def login_user(payload:LoginDTO, db: Session = Depends(get_db)):
    print(f"Login attempt for email: {payload.email}")
    return user_controller.login_user(db, payload.email, payload.password)

@router.get("/{user_id}", response_model=UserResponseDTO)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_controller.get_user(db, user_id)


@router.put("/{user_id}", response_model=UserResponseDTO)
def update_user(user_id: int, payload: UserUpdateDTO, db: Session = Depends(get_db)):
    return user_controller.update_user(db, user_id, payload)


@router.delete("/{user_id}", status_code=204)   
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_controller.delete_user(db, user_id)
    return None

@router.get("/", response_model=list[UserResponseDTO])
def list_users(db: Session = Depends(get_db)):
    return user_controller.list_users(db)
