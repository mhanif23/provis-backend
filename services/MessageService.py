from sqlalchemy.orm import Session
from models import model
from schemas import *

def createMessage(db: Session, message: MessageCreate):
    db_message = model.Message(
        patient_id=message.patient_id,
        doctor_id=message.doctor_id,
        datetime=message.datetime,
        text=message.text
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def readMessage(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()

def readMessages_byPatient(db: Session, patient_id: int, skip: int = 0, limit: int = 100):
    return db.query(Message).filter(Message.patient_id == patient_id).offset(skip).limit(limit).all()

def readMessages_byDoctor(db: Session, doctor_id: int, skip: int = 0, limit: int = 100):
    return db.query(Message).filter(Message.doctor_id == doctor_id).offset(skip).limit(limit).all()

def readMessages_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Message).offset(skip).limit(limit).all()

def deleteMessages_all(db: Session):
    row_affected = db.query(Message).delete()
    db.commit()
    return row_affected
