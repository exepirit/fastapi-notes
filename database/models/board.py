from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .base import Base


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    notes = relationship("Note", back_populates="board")
