from sqlalchemy.orm import Session
from models import model
from schemas import *
from sqlalchemy import desc
from .Auth import encrypt

def authenticate(db,user: UserSchema.UserCreate):
    user_auth = readUser_byUsername(db=db, username=user.username)
    if user_auth:
        return (user_auth.hashed_password == encrypt(user.password))
    else:
        return False    
    
def createUser(db: Session, user: UserCreate):
    hashed_password = encrypt(user.password)
    db_user = model.User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def readUser(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.id == user_id).first()

def readUser_byUsername(db: Session, username: str):
    return db.query(model.User).filter(model.User.username == username).first()

def readUser_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).offset(skip).limit(limit).all()

def deleteUser_all(db: Session):
    row_affected = db.query(model.User).delete()
    db.commit()
    return row_affected
