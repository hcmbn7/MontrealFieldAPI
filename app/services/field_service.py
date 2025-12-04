from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.field import Field
from app.models.field_schema import FieldCreate, FieldUpdate


def get_all_fields(db: Session):
    return db.query(Field).all()


def get_field_by_id(field_id: int, db: Session):
    field = db.query(Field).filter(Field.id == field_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Terrain non trouvé")
    return field


def create_field(field_data: FieldCreate, db: Session):
    db_field = Field(**field_data.dict())
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return db_field


def update_field(field_id: int, field_data: FieldUpdate, db: Session):
    field = get_field_by_id(field_id, db)
    update_payload = field_data.dict(exclude_unset=True)
    if not update_payload:
        return field
    for key, value in update_payload.items():
        setattr(field, key, value)
    db.add(field)
    db.commit()
    db.refresh(field)
    return field


def delete_field_by_id(field_id: int, db: Session):
    field = get_field_by_id(field_id, db)
    db.delete(field)
    db.commit()
