from pydantic import BaseModel


class NoteBase(BaseModel):
    text: str


class Note(NoteBase):
    id: int

    class Config:
        orm_mode = True
