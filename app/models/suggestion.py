from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class FieldSuggestion(Base):
    __tablename__ = "field_suggestions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    borough = Column(String, nullable=True)
    surface_type = Column(String, nullable=True)
    format = Column(String, nullable=True)
    status = Column(String, nullable=False, default="pending")
    published_field_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
