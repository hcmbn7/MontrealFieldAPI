from typing import List, Optional

from pydantic import BaseModel


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


class FieldUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    coordinates: Optional[List[float]] = None
    surface_type: Optional[str] = None
    format: Optional[str] = None
    lighting: Optional[bool] = None
    parking: Optional[bool] = None
    accessibility: Optional[bool] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    borough: Optional[str] = None
    description: Optional[str] = None
    amenities: Optional[List[str]] = None
    rating: Optional[float] = None
    reviews: Optional[int] = None
    photos: Optional[List[str]] = None


class FieldOut(FieldCreate):
    id: int

    class Config:
        orm_mode = True
