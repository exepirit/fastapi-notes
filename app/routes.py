from typing import List
from fastapi import HTTPException
from . import app
from database import crud, schemes, exceptions
from database.database import database


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/api/board", response_model=List[schemes.Board], response_model_exclude={"notes"},
         tags=["Board"])
async def get_boards():
    return await crud.get_boards()


@app.post("/api/board", response_model=schemes.Board, response_model_exclude={"board_id"},
          tags=["Board"])
async def add_board(board: schemes.BoardBase):
    return await crud.create_board(board)


@app.get("/api/board/{board_id}", response_model=schemes.Board, tags=["Board"])
async def get_board(board_id: int):
    try:
        return await crud.get_board(board_id)
    except exceptions.NotFoundError:
        raise HTTPException(status_code=404, detail="Board not found")


@app.delete("/api/board/{board_id}", tags=["Board"])
async def delete_board(board_id: int):
    await crud.delete_board(board_id)


@app.post("/api/note", response_model=schemes.Note, tags={"Note"})
async def add_note(board_id: int, note: schemes.NoteBase):
    if await crud.get_board(board_id) is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return await crud.create_note(board_id, note)


@app.delete("/api/note/{note_id}", tags={"Note"})
async def delete_note(note_id: int):
    await crud.delete_note(note_id)
