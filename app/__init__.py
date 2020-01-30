from fastapi import FastAPI
from config import Config

app = FastAPI(debug=Config.DEBUG)
