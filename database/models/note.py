from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    board_id = Column(Integer, ForeignKey("boards.id"))
    board = relationship("Board", back_populates="notes")
