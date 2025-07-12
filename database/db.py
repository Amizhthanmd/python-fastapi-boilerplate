import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import user

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'users.db')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    user.Base.metadata.create_all(bind=engine)
