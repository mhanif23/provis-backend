from sqlalchemy.orm import Session
from models import model
from schemas import *
from datetime import time

def createSchedule(db: Session, schedule: ScheduleCreate):
    db_schedule = model.Schedule(
        patient_id=schedule.patient_id,
        doctor_id=schedule.doctor_id,
        reservation_num=schedule.reservation_num,
        timestart=schedule.timestart.strftime("%H:%M:%S"),  # Convert time to string
        timeend=schedule.timeend.strftime("%H:%M:%S"),      # Convert time to string
        location=schedule.location,
        bpjs=schedule.bpjs,
        status=schedule.status
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def readSchedule(db: Session, schedule_id: int):
    db_schedule = db.query(model.Schedule).filter(model.Schedule.id == schedule_id).first()
    if db_schedule:
        db_schedule.timestart = time.fromisoformat(db_schedule.timestart)
        db_schedule.timeend = time.fromisoformat(db_schedule.timeend)
    return db_schedule

def readSchedule_byUser(db: Session, patient_id: int, skip: int = 0, limit: int = 100):
    schedules = db.query(model.Schedule).filter(model.Schedule.patient_id == patient_id).offset(skip).limit(limit).all()
    for schedule in schedules:
        schedule.timestart = time.fromisoformat(schedule.timestart)
        schedule.timeend = time.fromisoformat(schedule.timeend)
    return schedules

def readSchedule_byDoctor(db: Session, doctor_id: int, skip: int = 0, limit: int = 100):
    schedules = db.query(model.Schedule).filter(model.Schedule.doctor_id == doctor_id).offset(skip).limit(limit).all()
    for schedule in schedules:
        schedule.timestart = time.fromisoformat(schedule.timestart)
        schedule.timeend = time.fromisoformat(schedule.timeend)
    return schedules

def readSchedule_all(db: Session, skip: int = 0, limit: int = 100):
    schedules = db.query(model.Schedule).offset(skip).limit(limit).all()
    for schedule in schedules:
        schedule.timestart = time.fromisoformat(schedule.timestart)
        schedule.timeend = time.fromisoformat(schedule.timeend)
    return schedules

def deleteSchedule_all(db: Session):
    row_affected = db.query(model.Schedule).delete()
    db.commit()
    return row_affected
