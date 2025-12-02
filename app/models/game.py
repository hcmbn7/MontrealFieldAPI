from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=False, index=True)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    start_at = Column(DateTime, nullable=False, index=True)
    duration_minutes = Column(Integer, nullable=False, default=60)
    max_players = Column(Integer, nullable=False, default=10)
    skill_level = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="scheduled")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    participants = relationship(
        "GameParticipant",
        back_populates="game",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class GameParticipant(Base):
    __tablename__ = "game_participants"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    role = Column(String, nullable=False, default="player")
    status = Column(String, nullable=False, default="joined")  # joined | cancelled
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    game = relationship("Game", back_populates="participants")
