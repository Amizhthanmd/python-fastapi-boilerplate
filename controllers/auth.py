from sqlalchemy.orm import Session
from models.users import User
from schemas.users import Login
from utils import helpers
from fastapi import HTTPException

def get_user_by_userID(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()

def login(db: Session, user: Login):
    user_db = get_user_by_userID(db, user.user_id)
    if not user_db:
        raise HTTPException(status_code=400, detail="Invalid user id")
    
    if not helpers.verify_password(user.password, user_db.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token = helpers.create_access_token(data={
        "id": user_db.id,
        "email": user_db.user_id,
        "is_active": user_db.is_active,
    })

    return {"access_token": access_token, "message" : "Login successful", "Status" : True}
