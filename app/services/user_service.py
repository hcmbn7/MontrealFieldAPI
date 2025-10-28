from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.models.user_schema import UserCreate, UserLogin


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
    db_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        is_active=user_data.is_active,
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
