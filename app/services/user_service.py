from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.field import Field
from app.models.user import User
from app.models.user_schema import UserCreate, UserLogin


def _normalize_favorites(favorite_ids: list[int] | None) -> list[int]:
    if not favorite_ids:
        return []
    normalized = []
    for raw_id in favorite_ids:
        try:
            value = int(raw_id)
        except (TypeError, ValueError):
            continue
        normalized.append(value)
    return sorted(set(normalized))


def _ensure_field_exists(field_id: int, db: Session) -> None:
    exists = db.query(Field.id).filter(Field.id == field_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Terrain non trouvé")


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


def create_user(user_data: UserCreate, db: Session):
    if get_user_by_email(user_data.email, db):
        raise HTTPException(status_code=400, detail="L'adresse e-mail est déjà utilisée")
    favorites = _normalize_favorites(user_data.favorites)
    db_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        is_active=user_data.is_active,
        favorites=favorites,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_by_id(user_id: int, db: Session):
    user = get_user_by_id(user_id, db)
    db.delete(user)
    db.commit()


def authenticate_user(login_data: UserLogin, db: Session):
    user = get_user_by_email(login_data.email, db)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    return user


def get_user_favorites(user_id: int, db: Session) -> list[int]:
    user = get_user_by_id(user_id, db)
    return list(user.favorites or [])


def add_favorite_to_user(user_id: int, field_id: int, db: Session):
    user = get_user_by_id(user_id, db)
    _ensure_field_exists(field_id, db)
    favorites = set(user.favorites or [])
    if field_id in favorites:
        return user
    favorites.add(field_id)
    user.favorites = sorted(favorites)
    db.commit()
    db.refresh(user)
    return user


def remove_favorite_from_user(user_id: int, field_id: int, db: Session):
    user = get_user_by_id(user_id, db)
    favorites = set(user.favorites or [])
    if field_id not in favorites:
        return user
    favorites.remove(field_id)
    user.favorites = sorted(favorites)
    db.commit()
    db.refresh(user)
    return user


def replace_user_favorites(user_id: int, favorites: list[int], db: Session):
    user = get_user_by_id(user_id, db)
    normalized = _normalize_favorites(favorites)
    if normalized:
        # Validate that each referenced field exists
        missing = []
        for field_id in normalized:
            exists = db.query(Field.id).filter(Field.id == field_id).first()
            if not exists:
                missing.append(field_id)
        if missing:
            raise HTTPException(
                status_code=404,
                detail=f"Terrains introuvables: {', '.join(map(str, missing))}",
            )
    user.favorites = normalized
    db.commit()
    db.refresh(user)
    return user
