from typing import List
from . import tables
from . import schemes
from .database import database
from .exceptions import NotFoundError


async def create_board(board: schemes.BoardBase):
    query = tables.boards.insert().values(**board.dict(exclude={"notes"}))
    return await database.execute(query)


async def get_board(board_id: int) -> schemes.Board:
    board = await database.fetch_one(
        tables.boards.select().where(tables.boards.c.id == board_id)
    )
    if board is None:
        raise NotFoundError()
    notes = await database.fetch_all(
        tables.notes.select().where(tables.boards.c.id == board.id)
    )
    return schemes.Board(**board, notes=notes)


async def get_boards() -> List[schemes.Board]:
    query = tables.boards.select()
    return await database.fetch_all(query)


async def delete_board(board_id: int) -> bool:
    query = tables.boards.delete().where(tables.boards.c.id == board_id)
    return await database.execute(query) > 0


async def create_note(board_id: int, note: schemes.NoteBase) -> schemes.Note:
    query = tables.notes.insert().values(**note.dict(), board_id=board_id)
    return await database.fetch_one(query)


async def delete_note(note_id: int) -> bool:
    query = tables.notes.delete().where(tables.notes.c.id == note_id)
    return await database.execute(query) > 0
