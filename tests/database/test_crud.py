import pytest
from sqlalchemy.orm import Session
from database import crud
from database.models import Board, Note
from database.database import SessionLocal
from database.schemes import BoardBase, NoteBase


@pytest.fixture()
def database():
    db: Session = SessionLocal()
    db.query(Board).delete()
    db.query(Note).delete()
    yield db
    db.close()


def test__base_board__create_board__board_in_db(database):
    board = BoardBase(name="Test board 1")

    crud.create_board(database, board)

    db_board = database.query(Board).first()
    assert db_board.name == board.name


def test__board_in_db__get_board__are_equal(database):
    board_in_db = Board(name="Test board 2")
    database.add(board_in_db)
    database.commit()
    database.refresh(board_in_db)

    board = crud.get_board(database, board_in_db.id)
    assert board.name == board_in_db.name


def test__board_array__get_boards__len_is_equal(database):
    boards = [crud.create_board(database, BoardBase(name=f"Test board 3-{i}"))
              for i in range(0, 10)]

    boards_in_db = crud.get_boards(database)
    assert len(boards_in_db) == len(boards)


def test__board__delete_board__board_not_in_db(database):
    board = crud.create_board(database, BoardBase(name="Test board 4"))
    board_id = board.id

    crud.delete_board(database, Board(id=board.id, name="Test board 4"))

    boards = database.query(Board).filter(board_id == board).all()
    assert len(boards) == 0


def test__base_note__create_note__note_in_db(database):
    board = crud.create_board(database, BoardBase(name="Test board 5"))
    note_base = NoteBase(text="text")

    crud.create_note(database, board.id, note_base)

    note = database.query(Note).first()
    assert note.text == note_base.text
    assert note.board_id == board.id


def test__note_in_db__delete_note__note_not_in_db(database):
    board = crud.create_board(database, BoardBase(name="Test board 6"))
    note = crud.create_note(database, board.id, NoteBase(text="text 2"))

    crud.delete_note(database, note)

    note_in_db = database.query(Note).filter(Note.board_id == board.id).first()
    assert note_in_db is None
