from pydantic import BaseModel
from typing import Optional, List

class FieldCreate(BaseModel):
    name: str
    address: str
    coordinates: List[float]
    surface_type: Optional[str] = None
    format: Optional[str] = None
    lighting: Optional[bool] = False
    parking: Optional[bool] = False
    accessibility: Optional[bool] = False
    phone: Optional[str] = None
    website: Optional[str] = None
    borough: Optional[str] = None
    description: Optional[str] = None
    amenities: Optional[List[str]] = []
    rating: Optional[float] = None
    reviews: Optional[int] = None
    photos: Optional[List[str]] = []

class FieldOut(FieldCreate):
    id: int

    class Config:
        orm_mode = True

