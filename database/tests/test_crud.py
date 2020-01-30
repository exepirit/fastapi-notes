import unittest
from sqlalchemy.orm import Session
from config import Config

Config.DB_STRING = "sqlite:///:memory:"
from database import crud
from database.models import Board, Note
from database.database import SessionLocal
from database.schemes import BoardBase, NoteBase


class CrudTest(unittest.TestCase):
    db: Session

    @classmethod
    def setUpClass(cls) -> None:
        cls.db = SessionLocal()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.close()

    def setUp(self) -> None:
        self.db.query(Board).delete()
        self.db.query(Note).delete()

    def test__base_board__create_board__board_in_db(self):
        board = BoardBase(name="Test board 1")

        crud.create_board(self.db, board)

        db_board = self.db.query(Board).first()
        self.assertEqual(db_board.name, board.name)

    def test__board_in_db__get_board__are_equal(self):
        board_in_db = Board(name="Test board 2")
        self.db.add(board_in_db)
        self.db.commit()
        self.db.refresh(board_in_db)

        board = crud.get_board(self.db, board_in_db.id)

        self.assertEqual(board.name, board_in_db.name)

    def test__board_array__get_boards__len_is_equal(self):
        boards = [crud.create_board(self.db, BoardBase(name=f"Test board 3-{i}"))
                  for i in range(0, 10)]

        boards_in_db = crud.get_boards(self.db)

        self.assertEqual(len(boards_in_db), len(boards))

    def test__board__delete_board__board_not_in_db(self):
        board = crud.create_board(self.db, BoardBase(name="Test board 4"))
        board_id = board.id

        crud.delete_board(self.db, Board(id=board.id, name="Test board 4"))

        self.assertEqual(
            len(self.db.query(Board).filter(board_id == board).all()),
            0
        )

    def test__base_note__create_note__note_in_db(self):
        board = crud.create_board(self.db, BoardBase(name="Test board 5"))
        note_base = NoteBase(text="text")

        crud.create_note(self.db, board.id, note_base)

        note = self.db.query(Note).first()
        self.assertEqual(note.text, note_base.text)
        self.assertEqual(note.board_id, board.id)

    def test__note_in_db__delete_note__note_not_in_db(self):
        board = crud.create_board(self.db, BoardBase(name="Test board 6"))
        note = crud.create_note(self.db, board.id, NoteBase(text="text 2"))

        crud.delete_note(self.db, note)

        self.assertEqual(self.db.query(Note).filter(Note.board_id == board.id).first(), None)
