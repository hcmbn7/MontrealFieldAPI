from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.field import Field
from app.models.field_schema import FieldCreate, FieldUpdate

MAX_FEATURED_FIELDS = 3


def get_all_fields(db: Session):
    return db.query(Field).all()


def get_field_by_id(field_id: int, db: Session):
    field = db.query(Field).filter(Field.id == field_id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Terrain non trouvé")
    return field


def create_field(field_data: FieldCreate, db: Session):
    if field_data.featured:
        current_featured = db.query(Field).filter(Field.featured.is_(True)).count()
        if current_featured >= MAX_FEATURED_FIELDS:
            raise HTTPException(
                status_code=400,
                detail=f"Nombre maximum de terrains à la une atteint ({MAX_FEATURED_FIELDS}).",
            )
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
    new_featured_value = update_payload.get("featured")
    if new_featured_value is True and not field.featured:
        current_featured = (
            db.query(Field)
            .filter(Field.featured.is_(True), Field.id != field_id)
            .count()
        )
        if current_featured >= MAX_FEATURED_FIELDS:
            raise HTTPException(
                status_code=400,
                detail=f"Nombre maximum de terrains à la une atteint ({MAX_FEATURED_FIELDS}).",
            )
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
