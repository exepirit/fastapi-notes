from typing import List
from pydantic import BaseModel
from .note import Note


class BoardBase(BaseModel):
    name: str
    notes: List[Note] = []


class Board(BoardBase):
    id: int

    class Config:
        orm_mode = True
