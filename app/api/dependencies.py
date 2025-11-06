from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.admin import Admin
from app.services import admin_service

_basic_auth = HTTPBasic()


def get_current_admin(
    credentials: HTTPBasicCredentials = Depends(_basic_auth),
    db: Session = Depends(get_db),
) -> Admin:
    return admin_service.authenticate_admin_basic(credentials.username, credentials.password, db)
