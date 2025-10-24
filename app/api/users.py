from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user_schema import UserCreate, UserOut
from app.services import user_service

router = APIRouter()


@router.get("/users", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(user_id, db)


@router.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(user, db)


@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service.delete_user_by_id(user_id, db)
    return
