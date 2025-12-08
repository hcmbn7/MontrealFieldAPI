from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.db.database import Base


class GameHistory(Base):
    __tablename__ = "game_history"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    field_id = Column(Integer, nullable=False, index=True)
    organizer_id = Column(Integer, nullable=False, index=True)
    start_at = Column(DateTime, nullable=False, index=True)
    duration_minutes = Column(Integer, nullable=False)
    max_players = Column(Integer, nullable=False)
    skill_level = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    status = Column(String, nullable=False, default="completed")
    archived_at = Column(DateTime, nullable=False, default=datetime.utcnow)
