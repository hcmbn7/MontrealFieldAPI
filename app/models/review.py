from sqlalchemy import Column, Integer, String, DateTime, func, UniqueConstraint

from app.db.database import Base


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("user_id", "field_id", name="uq_review_user_field"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    field_id = Column(Integer, nullable=False, index=True)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
