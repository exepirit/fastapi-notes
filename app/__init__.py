from fastapi import FastAPI
from config import Config
from database.database import engine

app = FastAPI(debug=Config.DEBUG)

from . import routes
