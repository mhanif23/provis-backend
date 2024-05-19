from sqlalchemy.orm import Session
from models import model
from schemas import *
from sqlalchemy import desc

def createMedicine(db: Session, medicine: MedicineSchema.MedicineCreate):
    db_medicine = model.Medicine(
        name=medicine.name,
        manufacturer=medicine.manufacturer,
        dosage=medicine.dosage,
        description=medicine.description,
        instruction=medicine.instruction,
        price=medicine.price
    )
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine

def readMedicine(db: Session, medicine_id: int):
    return db.query(model.Medicine).filter(model.Medicine.id == medicine_id).first()

def readMedicine_byName(db: Session, name: str):
    return db.query(model.Medicine).filter(model.Medicine.name == name).first()

def readMedicine_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Medicine).offset(skip).limit(limit).all()

def deleteMedicine_all(db: Session):
    row_affected = db.query(model.Medicine).delete()
    db.commit()
    return row_affected