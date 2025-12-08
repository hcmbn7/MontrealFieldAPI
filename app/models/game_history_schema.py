from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class GameHistoryOut(BaseModel):
    id: int
    title: str
    field_id: int
    organizer_id: int
    start_at: datetime
    duration_minutes: int
    max_players: int
    skill_level: Optional[str] = None
    notes: Optional[str] = None
    status: str
    archived_at: datetime

    model_config = ConfigDict(from_attributes=True)
