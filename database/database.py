from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dynaconf import settings

engine = create_engine(settings.DB_STRING, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
