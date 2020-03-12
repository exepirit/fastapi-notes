from fastapi import FastAPI
from dynaconf import settings
from database.models import base
from database.database import SessionLocal, engine

base.Base.metadata.create_all(bind=engine)
app = FastAPI(debug=settings.DEBUG)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

from . import routes
