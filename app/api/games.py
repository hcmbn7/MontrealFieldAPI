from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.game_history_schema import GameHistoryOut
from app.models.game_schema import GameCreate, GameOut, GameUpdate
from app.services import game_service

router = APIRouter()


@router.get("/games", response_model=list[GameOut])
def list_games(
    field_id: Optional[int] = None,
    after: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    return game_service.list_games(db, field_id=field_id, after=after or datetime.utcnow())

@router.get("/games/history", response_model=list[GameHistoryOut])
def list_game_history(
    organizer_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return game_service.list_game_history(db, organizer_id=organizer_id)


@router.get("/games/{game_id}", response_model=GameOut)
def get_game(game_id: int, db: Session = Depends(get_db)):
    return game_service.get_game(game_id, db)


@router.post("/games", response_model=GameOut, status_code=201)
def create_game(payload: GameCreate, db: Session = Depends(get_db)):
    return game_service.create_game(payload, db)


@router.patch("/games/{game_id}", response_model=GameOut)
def update_game(game_id: int, payload: GameUpdate, db: Session = Depends(get_db)):
    return game_service.update_game(game_id, payload, db)


@router.delete("/games/{game_id}", status_code=204)
def delete_game(game_id: int, db: Session = Depends(get_db)):
    game_service.delete_game(game_id, db)
    return


@router.post("/games/{game_id}/join", response_model=GameOut)
def join_game(game_id: int, user_id: int, db: Session = Depends(get_db)):
    return game_service.join_game(game_id, user_id, db)


@router.post("/games/{game_id}/leave", response_model=GameOut)
def leave_game(game_id: int, user_id: int, db: Session = Depends(get_db)):
    return game_service.leave_game(game_id, user_id, db)


@router.post("/games/{game_id}/cancel", response_model=GameOut)
def cancel_game(game_id: int, user_id: int, db: Session = Depends(get_db)):
    return game_service.cancel_game(game_id, user_id, db)
