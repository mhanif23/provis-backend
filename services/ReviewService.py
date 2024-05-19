from sqlalchemy.orm import Session
from models import model
from schemas import *

def createReview(db: Session, review: ReviewCreate):
    db_review = model.Review(
        patient_id=review.patient_id,
        doctor_id=review.doctor_id,
        text=review.text,
        date=review.date,
        star=review.star
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def readReview(db: Session, review_id: int):
    return db.query(model.Review).filter(model.Review.id == review_id).first()

def readReview_byUser(db: Session, patient_id: int, skip: int = 0, limit: int = 100):
    return db.query(model.Review).filter(model.Review.patient_id == patient_id).offset(skip).limit(limit).all()

def readReview_byDoctor(db: Session, doctor_id: int, skip: int = 0, limit: int = 100):
    return db.query(model.Review).filter(model.Review.doctor_id == doctor_id).offset(skip).limit(limit).all()

def readReview_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Review).offset(skip).limit(limit).all()

def deleteReview_all(db: Session):
    row_affected = db.query(model.Review).delete()
    db.commit()
    return row_affected
