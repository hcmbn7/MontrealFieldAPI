from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.field_schema import FieldCreate
from app.models.suggestion import FieldSuggestion
from app.models.suggestion_schema import SuggestionCreate, SuggestionUpdate
from app.services import field_service


def _get_suggestion_or_404(suggestion_id: int, db: Session) -> FieldSuggestion:
    suggestion = db.query(FieldSuggestion).filter(FieldSuggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion introuvable")
    return suggestion


def create_suggestion(payload: SuggestionCreate, db: Session) -> FieldSuggestion:
    suggestion = FieldSuggestion(**payload.dict())
    db.add(suggestion)
    db.commit()
    db.refresh(suggestion)
    return suggestion


def list_suggestions(db: Session):
    return db.query(FieldSuggestion).order_by(FieldSuggestion.created_at.desc()).all()


def update_suggestion(suggestion_id: int, payload: SuggestionUpdate, db: Session) -> FieldSuggestion:
    suggestion = _get_suggestion_or_404(suggestion_id, db)
    updates = payload.dict(exclude_unset=True)
    if not updates:
        return suggestion
    for key, value in updates.items():
        setattr(suggestion, key, value)
    db.add(suggestion)
    db.commit()
    db.refresh(suggestion)
    return suggestion


def delete_suggestion(suggestion_id: int, db: Session) -> None:
    suggestion = _get_suggestion_or_404(suggestion_id, db)
    db.delete(suggestion)
    db.commit()


def publish_suggestion(suggestion_id: int, db: Session):
    suggestion = _get_suggestion_or_404(suggestion_id, db)
    if suggestion.latitude is None or suggestion.longitude is None:
        raise HTTPException(
            status_code=400,
            detail="Latitude et longitude sont nécessaires pour publier ce terrain.",
        )
    payload = FieldCreate(
        name=suggestion.name,
        address=suggestion.address,
        coordinates=[suggestion.latitude, suggestion.longitude],
        surface_type=suggestion.surface_type,
        format=suggestion.format,
        description=suggestion.description,
        borough=suggestion.borough,
        lighting=False,
        parking=False,
        accessibility=False,
        phone=None,
        website=None,
        amenities=[],
        rating=None,
        reviews=None,
        photos=[],
    )

    field = field_service.create_field(payload, db)
    suggestion.status = "published"
    suggestion.published_field_id = field.id
    db.add(suggestion)
    db.commit()
    db.refresh(suggestion)
    return suggestion
