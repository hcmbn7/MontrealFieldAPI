from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.field import Field
from app.models.game import Game, GameParticipant
from app.models.game_history import GameHistory
from app.models.game_schema import GameCreate, GameUpdate
from app.models.user import User


def _to_utc_naive(dt: datetime) -> datetime:
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def _ensure_field_exists(field_id: int, db: Session):
    exists = db.query(Field.id).filter(Field.id == field_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Terrain non trouvé")


def _ensure_user_exists(user_id: int, db: Session):
    exists = db.query(User.id).filter(User.id == user_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")


def archive_past_games(db: Session):
    now = datetime.utcnow()
    past_games = db.query(Game).filter(Game.start_at < now).all()
    if not past_games:
        return
    for game in past_games:
        if game.status == "cancelled":
            db.delete(game)
            continue
        history = GameHistory(
            title=game.title,
            field_id=game.field_id,
            organizer_id=game.organizer_id,
            start_at=game.start_at,
            duration_minutes=game.duration_minutes,
            max_players=game.max_players,
            skill_level=game.skill_level,
            notes=game.notes,
            status=game.status,
            archived_at=now,
        )
        db.add(history)
        db.delete(game)
    db.commit()


def list_games(db: Session, field_id: int | None = None, after: datetime | None = None):
    archive_past_games(db)
    query = db.query(Game).order_by(Game.start_at.asc())
    if field_id is not None:
        query = query.filter(Game.field_id == field_id)
    if after is not None:
        query = query.filter(Game.start_at >= _to_utc_naive(after))
    return query.all()


def get_game(game_id: int, db: Session):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Match introuvable")
    return game


def create_game(payload: GameCreate, db: Session):
    _ensure_field_exists(payload.field_id, db)
    _ensure_user_exists(payload.organizer_id, db)

    start_at = _to_utc_naive(payload.start_at)

    if start_at <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="La date doit être dans le futur")

    game = Game(
        title=payload.title.strip(),
        field_id=payload.field_id,
        organizer_id=payload.organizer_id,
        start_at=start_at,
        duration_minutes=payload.duration_minutes,
        max_players=payload.max_players,
        skill_level=payload.skill_level,
        notes=payload.notes,
        status="scheduled",
    )
    db.add(game)
    db.flush()

    organizer_participant = GameParticipant(
        game_id=game.id,
        user_id=payload.organizer_id,
        role="organizer",
        status="joined",
    )
    db.add(organizer_participant)

    db.commit()
    db.refresh(game)
    return game


def update_game(game_id: int, payload: GameUpdate, db: Session):
    game = get_game(game_id, db)

    updates = payload.dict(exclude_unset=True)
    if not updates:
        return game

    if "start_at" in updates and updates["start_at"] is not None:
        updates["start_at"] = _to_utc_naive(updates["start_at"])
        if updates["start_at"] <= datetime.utcnow():
            raise HTTPException(status_code=400, detail="La date doit être dans le futur")

    for key, value in updates.items():
        setattr(game, key, value)

    db.commit()
    db.refresh(game)
    return game


def delete_game(game_id: int, db: Session):
    game = get_game(game_id, db)
    db.delete(game)
    db.commit()


def join_game(game_id: int, user_id: int, db: Session):
    game = get_game(game_id, db)
    _ensure_user_exists(user_id, db)

    if game.status == "cancelled":
        raise HTTPException(status_code=400, detail="Ce match est annulé")

    existing = (
        db.query(GameParticipant)
        .filter(GameParticipant.game_id == game_id, GameParticipant.user_id == user_id)
        .first()
    )
    if existing:
        return game

    active_count = (
        db.query(GameParticipant)
        .filter(GameParticipant.game_id == game_id, GameParticipant.status == "joined")
        .count()
    )
    if active_count >= game.max_players:
        raise HTTPException(status_code=400, detail="Ce match est complet")

    participant = GameParticipant(
        game_id=game_id,
        user_id=user_id,
        role="player",
        status="joined",
    )
    db.add(participant)
    db.commit()
    db.refresh(game)
    return game


def leave_game(game_id: int, user_id: int, db: Session):
    game = get_game(game_id, db)
    participant = (
        db.query(GameParticipant)
        .filter(GameParticipant.game_id == game_id, GameParticipant.user_id == user_id)
        .first()
    )
    if not participant:
        return game

    db.delete(participant)
    db.commit()
    db.refresh(game)
    return game


def cancel_game(game_id: int, user_id: int, db: Session):
    game = get_game(game_id, db)
    if game.organizer_id != user_id:
        raise HTTPException(status_code=403, detail="Seul l'organisateur peut annuler le match")
    game.status = "cancelled"
    db.commit()
    db.refresh(game)
    return game


def list_game_history(db: Session, organizer_id: int | None = None):
    archive_past_games(db)
    query = db.query(GameHistory).order_by(GameHistory.start_at.desc())
    if organizer_id is not None:
        query = query.filter(GameHistory.organizer_id == organizer_id)
    return query.all()
