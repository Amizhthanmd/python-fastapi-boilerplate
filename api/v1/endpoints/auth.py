from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import auth
from schemas.users import Login
from database.db import get_db

auth_router = APIRouter()

@auth_router.post("/login")
async def login(user: Login, db: Session = Depends(get_db)):
    return auth.login(db, user)
