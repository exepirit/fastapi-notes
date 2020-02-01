from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy import MetaData

metadata = MetaData()


boards = Table(
    "boards", metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String)
)

notes = Table(
    "notes", metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("text", String),
    Column("board_id", Integer, ForeignKey("boards.id"), nullable=False)
)
