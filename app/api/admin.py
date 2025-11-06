from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin
from app.db.session import get_db
from app.models.admin import Admin
from app.models.admin_schema import AdminLogin, AdminOut
from app.services import admin_service

router = APIRouter()


@router.post("/admin/login", response_model=AdminOut)
def login_admin(credentials: AdminLogin, db: Session = Depends(get_db)):
    return admin_service.authenticate_admin(credentials, db)


@router.get("/admin/me", response_model=AdminOut)
def get_current_admin_profile(current_admin: Admin = Depends(get_current_admin)):
    return current_admin
