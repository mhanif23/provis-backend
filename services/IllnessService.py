from sqlalchemy.orm import Session
from models import model
from schemas import *

def createIllness(db: Session, illness: IllnessCreate):
    dbIllness = model.Illness(
        name=illness.name,
        category=illness.category,
        general_symptoms=illness.general_symptoms,
        unique_symptoms=illness.unique_symptoms,
        extra_symptoms=illness.extra_symptoms
    )
    db.add(dbIllness)
    db.commit()
    db.refresh(dbIllness)
    return dbIllness

def readIllness(db: Session, illness_id: int):
    return db.query(model.Illness).filter(model.Illness.id == illness_id).first()

def readIllness_byCategory(db: Session, category: str, skip: int = 0, limit: int = 100):
    return db.query(model.Illness).filter(model.Illness.category == category).offset(skip).limit(limit).all()

def readIllness_byName(db: Session, name: str, skip: int = 0, limit: int = 100):
    return db.query(model.Illness).filter(model.Illness.name == name).offset(skip).limit(limit).all()

def readIllness_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Illness).offset(skip).limit(limit).all()

def deleteIllness_all(db: Session):
    rowAffected = db.query(model.Illness).delete()
    db.commit()
    return rowAffected
