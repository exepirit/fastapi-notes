from typing import List
from sqlalchemy.orm import Session
from . import models
from . import schemes


def create_board(db: Session, board: schemes.BoardBase) -> models.Board:
    db_board = models.Board(**board.dict())
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board


def get_board(db: Session, board_id: int) -> models.Board:
    return db.query(models.Board).filter(models.Board.id == board_id).first()


def get_boards(db: Session) -> List[models.Board]:
    return db.query(models.Board).all()


def delete_board(db: Session, board: schemes.Board) -> None:
    db.query(models.Board).filter(models.Board.id == board.id).delete()


def create_note(db: Session, board_id: int, note: schemes.NoteBase) -> models.Note:
    raise Exception("implement me")


def delete_note(db: Session, note: schemes.NoteBase) -> bool:
    raise Exception("implement me")
