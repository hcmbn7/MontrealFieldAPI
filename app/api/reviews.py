from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.review_schema import ReviewCreate, ReviewOut
from app.services import review_service

router = APIRouter()


@router.get("/fields/{field_id}/reviews", response_model=list[ReviewOut])
def list_reviews(field_id: int, db: Session = Depends(get_db)):
    return review_service.get_reviews_for_field(field_id, db)


@router.get("/fields/{field_id}/reviews/{user_id}", response_model=ReviewOut)
def get_review(field_id: int, user_id: int, db: Session = Depends(get_db)):
    return review_service.get_review_for_user(field_id, user_id, db)


@router.put("/fields/{field_id}/reviews/{user_id}", response_model=ReviewOut)
def upsert_review(
    field_id: int,
    user_id: int,
    payload: ReviewCreate,
    db: Session = Depends(get_db),
):
    return review_service.upsert_review(field_id, user_id, payload, db)


@router.delete("/fields/{field_id}/reviews/{user_id}", status_code=204)
def delete_review(field_id: int, user_id: int, db: Session = Depends(get_db)):
    review_service.delete_review(field_id, user_id, db)
    return
