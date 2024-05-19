from sqlalchemy.orm import Session
from models import model
from schemas import *

def createNotification(db: Session, notification: NotificationCreate):
    db_notification = model.Notification(
        patient_id=notification.patient_id,
        message=notification.message
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def readNotification(db: Session, notification_id: int):
    return db.query(model.Notification).filter(model.Notification.id == notification_id).first()

def readNotification_byUser(db: Session, patient_id: int, skip: int = 0, limit: int = 100):
    return db.query(model.Notification).filter(model.Notification.patient_id == patient_id).offset(skip).limit(limit).all()

def readNotification_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Notification).offset(skip).limit(limit).all()

def deleteNotification_all(db: Session):
    row_affected = db.query(model.Notification).delete()
    db.commit()
    return row_affected
