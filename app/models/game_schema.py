from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class GameParticipantOut(BaseModel):
    user_id: int
    role: str = "player"
    status: str = "joined"
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GameBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    field_id: int
    organizer_id: int
    start_at: datetime
    duration_minutes: int = Field(default=60, ge=15, le=300)
    max_players: int = Field(default=10, ge=2, le=40)
    skill_level: Optional[str] = None
    notes: Optional[str] = None


class GameCreate(GameBase):
    pass


class GameUpdate(BaseModel):
    title: Optional[str] = None
    start_at: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(default=None, ge=15, le=300)
    max_players: Optional[int] = Field(default=None, ge=2, le=40)
    skill_level: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class GameOut(BaseModel):
    id: int
    title: str
    field_id: int
    organizer_id: int
    start_at: datetime
    duration_minutes: int
    max_players: int
    skill_level: Optional[str]
    notes: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    participants: List[GameParticipantOut] = []

    model_config = ConfigDict(from_attributes=True)
