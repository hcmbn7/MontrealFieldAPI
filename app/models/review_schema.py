from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = None


class ReviewCreate(ReviewBase):
    pass


class ReviewOut(ReviewBase):
    id: int
    user_id: int
    field_id: int
    created_at: datetime
    updated_at: datetime | None = None
    user_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
