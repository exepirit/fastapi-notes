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


def delete_board(db: Session, board: schemes.Board) -> bool:
    return db.query(models.Board).filter(models.Board.id == board.id).delete() > 0


def create_note(db: Session, board_id: int, note: schemes.NoteBase) -> models.Note:
    note_db = models.Note(board_id=board_id, **note.dict())
    db.add(note_db)
    db.commit()
    db.refresh(note_db)
    return note_db


def delete_note(db: Session, note: schemes.Note) -> bool:
    return db.query(models.Note).filter(models.Note.id == note.id).delete() > 0
