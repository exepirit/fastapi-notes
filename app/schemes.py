from typing import List
from pydantic import BaseModel


class Note(BaseModel):
    text: str


class Board(BaseModel):
    name: str
    notes: List[Note]
