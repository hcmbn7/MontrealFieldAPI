from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin
from app.models.admin import Admin
from app.db.session import get_db
from app.models.field_schema import FieldCreate, FieldOut, FieldUpdate
from app.services import field_service

router = APIRouter()

@router.get("/fields", response_model=list[FieldOut])
def get_fields(db: Session = Depends(get_db)):
    return field_service.get_all_fields(db)

@router.get("/fields/{field_id}", response_model=FieldOut)
def get_field(field_id: int, db: Session = Depends(get_db)):
    return field_service.get_field_by_id(field_id, db)

@router.post("/fields", response_model=FieldOut, status_code=201)
def create_field(
    field: FieldCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return field_service.create_field(field, db)

@router.put("/fields/{field_id}", response_model=FieldOut)
def update_field(
    field_id: int,
    field_update: FieldUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return field_service.update_field(field_id, field_update, db)

@router.delete("/fields/{field_id}", status_code=204)
def delete_field(
    field_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    field_service.delete_field_by_id(field_id, db)
    return

