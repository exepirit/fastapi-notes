from sqlalchemy import create_engine
from databases import Database
from config import Config
from .tables import metadata

database = Database(Config.DB_STRING)
engine = create_engine(Config.DB_STRING, connect_args={"check_same_thread": False})
metadata.create_all(engine)
