from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.admin import Admin
from app.models.admin_schema import AdminLogin


def get_admin_by_email(email: str, db: Session) -> Admin | None:
    return db.query(Admin).filter(Admin.email == email).first()


def authenticate_admin(credentials: AdminLogin, db: Session) -> Admin:
    admin = get_admin_by_email(credentials.email, db)
    if not admin or not verify_password(credentials.password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants administrateur invalides")
    return admin


def authenticate_admin_basic(email: str, password: str, db: Session) -> Admin:
    admin = get_admin_by_email(email, db)
    if not admin or not verify_password(password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants administrateur invalides")
    return admin
