from sqlalchemy.orm import Session
from models import model
from schemas import *

def createDiagnosis(db: Session, diagnosis: DiagnosisCreate):
    db_diagnosis = model.Diagnosis(
        diagnosis_name=diagnosis.diagnosis_name,
        recommendation=diagnosis.recommendation,
        medicine_recommendation=diagnosis.medicine_recommendation,
        doctor_id=diagnosis.doctor_id,
        patient_id=diagnosis.patient_id
    )
    db.add(db_diagnosis)
    db.commit()
    db.refresh(db_diagnosis)
    return db_diagnosis

def readDiagnosis(db: Session, diagnosis_id: int):
    return db.query(model.Diagnosis).filter(model.Diagnosis.id == diagnosis_id).first()

def readDiagnosis_byUser(db: Session, patient_id: int, skip: int = 0, limit: int = 100):
    return db.query(model.Diagnosis).filter(model.Diagnosis.patient_id == patient_id).offset(skip).limit(limit).all()

def readDiagnosis_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Diagnosis).offset(skip).limit(limit).all()

def deleteDiagnosis_all(db: Session):
    row_affected = db.query(model.Diagnosis).delete()
    db.commit()
    return row_affected
