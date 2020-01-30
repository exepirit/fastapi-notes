from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from . import app, get_db
from database import crud, schemes


@app.get("/api/board", response_model=List[schemes.Board], response_model_exclude={"notes"})
def get_boards(db: Session = Depends(get_db)):
    return crud.get_boards(db)


@app.post("/api/board", response_model=schemes.Board, response_model_exclude={"board_id"})
async def add_board(board: schemes.BoardBase, db: Session = Depends(get_db)):
    return await crud.create_board(db, board)


@app.get("/api/board/{board_id}", response_model=schemes.Board)
def get_board(board_id: int, db: Session = Depends(get_db)):
    board = crud.get_board(db, board_id)
    return board


@app.delete("/api/board/{board_id}")
async def delete_board(board_id: int, db: Session = Depends(get_db)):
    board = schemes.Board(id=board_id)
    if not crud.delete_board(db, board):
        raise HTTPException(status_code=404)


@app.post("/api/note", response_model=schemes.Note)
async def add_note(note: schemes.Note, db: Session = Depends(get_db)):
    if crud.get_board(db, note.board_id) is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return await crud.create_note(db, note)


@app.delete("/api/note/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = schemes.Note(id=note_id, board_id=-1)
    return crud.delete_note(db, note)
