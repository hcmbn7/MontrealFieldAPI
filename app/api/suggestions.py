from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin
from app.db.session import get_db
from app.models.admin import Admin
from app.models.suggestion_schema import (
    SuggestionCreate,
    SuggestionOut,
    SuggestionUpdate,
)
from app.services import suggestion_service

router = APIRouter()


@router.post("/field-suggestions", response_model=SuggestionOut, status_code=201)
def create_suggestion(payload: SuggestionCreate, db: Session = Depends(get_db)):
    return suggestion_service.create_suggestion(payload, db)


@router.get("/field-suggestions", response_model=list[SuggestionOut])
def list_suggestions(
    db: Session = Depends(get_db), current_admin: Admin = Depends(get_current_admin)
):
    return suggestion_service.list_suggestions(db)


@router.patch("/field-suggestions/{suggestion_id}", response_model=SuggestionOut)
def update_suggestion(
    suggestion_id: int,
    payload: SuggestionUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return suggestion_service.update_suggestion(suggestion_id, payload, db)


@router.delete("/field-suggestions/{suggestion_id}", status_code=204)
def delete_suggestion(
    suggestion_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    suggestion_service.delete_suggestion(suggestion_id, db)
    return


@router.post("/field-suggestions/{suggestion_id}/publish", response_model=SuggestionOut)
def publish_suggestion(
    suggestion_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    return suggestion_service.publish_suggestion(suggestion_id, db)
