from sqlalchemy.orm import Session
from models import model
from schemas import *
from sqlalchemy import desc

def calculate_age(birth_date: str) -> int:
    birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def createPatient(db: Session, patient: PatientCreate):
    age = calculate_age(patient.date_of_birth)
    db_patient = model.Patient(
        user_id=patient.user_id, 
        name=patient.name, 
        medical_record=patient.medical_record, 
        nik=patient.nik, 
        gender=patient.gender,
        address=patient.address, 
        telephone=patient.telephone,
        date_of_birth=patient.date_of_birth, 
        allergy=patient.allergy,
        allergy_year=patient.allergy_year,
        bpjs_status=patient.bpjs_status,
        height=patient.height,
        weight=patient.weight,
        bmi=patient.bmi,
        age=age
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

# def update_patient(db: Session, patient_id: int, patient: PatientSchema.PatientUpdate):
#     db_patient = db.query(model.Patient).filter(model.Patient.id == patient_id).first()
#     for key, value in patient.dict().items():
#         setattr(db_patient, key, value)
#     db.commit()
#     db.refresh(db_patient)
#     return db_patient

def readPatient(db: Session, patient_id: int):
    return db.query(model.Patient).filter(model.Patient.id == patient_id).first()

def readPatient_byName(db: Session, name: str):
    return db.query(model.Patient).filter(model.Patient.name == name).first()

def readPatient_byUID(db: Session, user_id: str):
    return db.query(model.Patient).filter(model.Patient.user_id == user_id).first()

def readPatient_nameAll(db: Session, name: str, skip: int = 0, limit: int = 100):
    return db.query(model.Patient).filter(model.Patient.name.like(f"%{name}%")).offset(skip).limit(limit).all()
    
def readPatient_specialtyAll(db: Session, specialty: str, skip: int = 0, limit: int = 100):
    return db.query(model.Patient).filter(model.Patient.specialty.like(f"%{specialty}%")).offset(skip).limit(limit).all()

def readPatient_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Patient).offset(skip).limit(limit).all()

def deletePatient_all(db: Session):
    row_affected = db.query(model.Patient).delete()
    db.commit()
    return row_affected

def get_patient(db: Session, patient_id: int):
    return db.query(model.Patient).filter(model.Patient.id == patient_id).first()

def update_patient(db: Session, patient_id: int, patient: PatientUpdate):
    db_patient = db.query(model.Patient).filter(model.Patient.user_id == patient_id).first()
    if db_patient is None:
        return None

    for key, value in patient.dict().items():
        setattr(db_patient, key, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient