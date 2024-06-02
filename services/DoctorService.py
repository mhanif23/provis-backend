from sqlalchemy.orm import Session
from models import model
from schemas import *
from sqlalchemy import desc

def createDoctor(db: Session, doctor: DoctorCreate):
    db_doctor = model.Doctor(name=doctor.name, user_id=doctor.user_id, specialty=doctor.specialty,
                              hospital=doctor.hospital, experience=doctor.experience,
                              philosophy=doctor.philosophy, innovation=doctor.innovation)
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def readDoctor(db: Session, doctor_id: int):
    return db.query(model.Doctor).filter(model.Doctor.id == doctor_id).first()

def readDoctor_byName(db: Session, name: str):
    return db.query(model.Doctor).filter(model.Doctor.name == name).first()

def readDoctor_byUID(db: Session, user_id: int):
    return db.query(model.Doctor).filter(model.Doctor.user_id == user_id).first()

def readDoctor_nameAll(db: Session, name: str, skip: int = 0, limit: int = 100):
    return db.query(model.Doctor).filter(model.Doctor.name.like(f"%{name}%")).offset(skip).limit(limit).all()
    
def readDoctor_specialtyAll(db: Session, specialty: str, skip: int = 0, limit: int = 100):
    return db.query(model.Doctor).filter(model.Doctor.specialty.like(f"%{specialty}%")).offset(skip).limit(limit).all()

def readDoctor_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Doctor).offset(skip).limit(limit).all()

def deleteDoctor_all(db: Session):
    row_affected = db.query(model.Doctor).delete()
    db.commit()
    return row_affected