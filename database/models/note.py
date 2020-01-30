from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    board = relationship("Board", back_populates="notes")
