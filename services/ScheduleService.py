from sqlalchemy.orm import Session
from models import model
from schemas import *

def createSchedule(db: Session, schedule: ScheduleCreate):
    db_schedule = model.Schedule(
        patient_id=schedule.patient_id,
        doctor_id=schedule.doctor_id,
        reservation_num=schedule.reservation_num,
        time=schedule.time,
        location=schedule.location
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def readSchedule(db: Session, schedule_id: int):
    return db.query(model.Schedule).filter(model.Schedule.id == schedule_id).first()

def readSchedule_byUser(db: Session, patient_id: int, skip: int = 0, limit: int = 100):
    return db.query(model.Schedule).filter(model.Schedule.patient_id == patient_id).offset(skip).limit(limit).all()

def readSchedule_byDoctor(db: Session, doctor_id: int, skip: int = 0, limit: int = 100):
    return db.query(model.Schedule).filter(model.Schedule.doctor_id == doctor_id).offset(skip).limit(limit).all()

def readSchedule_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Schedule).offset(skip).limit(limit).all()

def deleteSchedule_all(db: Session):
    row_affected = db.query(model.Schedule).delete()
    db.commit()
    return row_affected
