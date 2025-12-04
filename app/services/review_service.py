from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.field import Field
from app.models.review import Review
from app.models.review_schema import ReviewCreate
from app.models.user import User


def _ensure_user_exists(user_id: int, db: Session) -> None:
    exists = db.query(User.id).filter(User.id == user_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvAc")


def _ensure_field_exists(field_id: int, db: Session) -> None:
    exists = db.query(Field.id).filter(Field.id == field_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Terrain non trouvAc")


def _get_user_map(user_ids: set[int], db: Session) -> dict[int, str]:
    if not user_ids:
        return {}
    rows = db.query(User.id, User.full_name).filter(User.id.in_(user_ids)).all()
    return {row.id: row.full_name for row in rows}


def _serialize_review(review: Review, user_map: dict[int, str]):
    return {
        "id": review.id,
        "user_id": review.user_id,
        "field_id": review.field_id,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at,
        "updated_at": review.updated_at,
        "user_name": user_map.get(review.user_id),
    }


def _serialize_reviews(reviews: list[Review], db: Session):
    user_ids = {review.user_id for review in reviews}
    user_map = _get_user_map(user_ids, db)
    return [_serialize_review(review, user_map) for review in reviews]


def _recompute_field_rating(field_id: int, db: Session) -> None:
    avg_rating, review_count = (
        db.query(func.avg(Review.rating), func.count(Review.id))
        .filter(Review.field_id == field_id)
        .one()
    )
    field = db.query(Field).filter(Field.id == field_id).first()
    if not field:
        return
    field.rating = float(avg_rating) if review_count else None
    field.reviews = int(review_count or 0)
    db.add(field)


def get_reviews_for_field(field_id: int, db: Session):
    _ensure_field_exists(field_id, db)
    reviews = (
        db.query(Review)
        .filter(Review.field_id == field_id)
        .order_by(Review.created_at.desc())
        .all()
    )
    return _serialize_reviews(reviews, db)


def get_review_for_user(field_id: int, user_id: int, db: Session):
    _ensure_field_exists(field_id, db)
    _ensure_user_exists(user_id, db)
    review = (
        db.query(Review)
        .filter(Review.field_id == field_id, Review.user_id == user_id)
        .first()
    )
    if not review:
        raise HTTPException(status_code=404, detail="Avis non trouvAc")
    user_map = _get_user_map({review.user_id}, db)
    return _serialize_review(review, user_map)


def upsert_review(field_id: int, user_id: int, review_data: ReviewCreate, db: Session):
    _ensure_field_exists(field_id, db)
    _ensure_user_exists(user_id, db)
    review = (
        db.query(Review)
        .filter(Review.field_id == field_id, Review.user_id == user_id)
        .first()
    )

    if review:
        review.rating = review_data.rating
        review.comment = review_data.comment
    else:
        review = Review(
            field_id=field_id,
            user_id=user_id,
            rating=review_data.rating,
            comment=review_data.comment,
        )
        db.add(review)

    db.flush()
    _recompute_field_rating(field_id, db)
    db.commit()
    db.refresh(review)
    user_map = _get_user_map({review.user_id}, db)
    return _serialize_review(review, user_map)


def delete_review(field_id: int, user_id: int, db: Session) -> None:
    _ensure_field_exists(field_id, db)
    _ensure_user_exists(user_id, db)
    review = (
        db.query(Review)
        .filter(Review.field_id == field_id, Review.user_id == user_id)
        .first()
    )
    if not review:
        raise HTTPException(status_code=404, detail="Avis non trouvAc")

    db.delete(review)
    db.flush()
    _recompute_field_rating(field_id, db)
    db.commit()
