from sqlalchemy.orm import Session
from models import model
from schemas import *
from sqlalchemy import desc

def createHospital(db: Session, hospital: HospitalSchema.HospitalCreate):
    db_hospital = model.Hospital(
        name=hospital.name,
        address=hospital.address,
        longitude=hospital.longitude,
        latitude=hospital.latitude,
    )
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

def readHospital(db: Session, hospital_id: int):
    return db.query(model.Hospital).filter(model.Hospital.id == hospital_id).first()

def readHospital_byName(db: Session, name: str):
    return db.query(model.Hospital).filter(model.Hospital.name == name).first()

def readHospital_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Hospital).offset(skip).limit(limit).all()

def deleteHospital_all(db: Session):
    row_affected = db.query(model.Hospital).delete()
    db.commit()
    return row_affected