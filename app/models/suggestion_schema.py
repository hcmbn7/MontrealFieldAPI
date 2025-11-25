from typing import Optional

from pydantic import BaseModel, ConfigDict


class SuggestionBase(BaseModel):
    name: str
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    contact: Optional[str] = None
    borough: Optional[str] = None
    surface_type: Optional[str] = None
    format: Optional[str] = None


class SuggestionCreate(SuggestionBase):
    pass


class SuggestionUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    contact: Optional[str] = None
    borough: Optional[str] = None
    surface_type: Optional[str] = None
    format: Optional[str] = None
    status: Optional[str] = None
    published_field_id: Optional[int] = None


class SuggestionOut(SuggestionBase):
    id: int
    status: str
    published_field_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
