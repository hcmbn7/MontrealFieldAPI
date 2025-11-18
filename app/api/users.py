from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user_schema import (
    UserCreate,
    UserOut,
    UserLogin,
    UserFavoritesUpdate,
    UserUpdate,
)
from app.services import user_service

router = APIRouter()


@router.get("/users", response_model=list[UserOut])
def get_users(
    email: Optional[str] = None, db: Session = Depends(get_db)
):
    if email:
        user = user_service.get_user_by_email(email, db)
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        return [user]
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


@router.post("/users/login", response_model=UserOut)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    return user_service.authenticate_user(user, db)


@router.get("/users/{user_id}/favorites", response_model=list[int])
def get_user_favorites(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_favorites(user_id, db)


@router.post("/users/{user_id}/favorites/{field_id}", response_model=UserOut)
def add_favorite(user_id: int, field_id: int, db: Session = Depends(get_db)):
    return user_service.add_favorite_to_user(user_id, field_id, db)


@router.delete("/users/{user_id}/favorites/{field_id}", response_model=UserOut)
def remove_favorite(user_id: int, field_id: int, db: Session = Depends(get_db)):
    return user_service.remove_favorite_from_user(user_id, field_id, db)


@router.put("/users/{user_id}/favorites", response_model=UserOut)
def replace_favorites(
    user_id: int,
    payload: UserFavoritesUpdate,
    db: Session = Depends(get_db),
):
    return user_service.replace_user_favorites(user_id, payload.favorites, db)


@router.patch("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
):
    return user_service.update_user(user_id, payload, db)
