import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # E:\FarmHub
DB_PATH = os.path.join(BASE_DIR, "core", "db.sqlite3")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
print('db path : ', SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
print('engine : ', engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()















