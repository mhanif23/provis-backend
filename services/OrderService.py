from sqlalchemy.orm import Session
from models import model
from schemas import OrderCreate

def createOrder(db: Session, order: OrderCreate):
    db_order = model.Order(
        patient_id=order.patient_id,
        medicine_id=order.medicine_id,
        address=order.address,
        courier=order.courier,
        payment=order.payment,
        bpjs=order.bpjs,
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def readOrder(db: Session, order_id: int):
    return db.query(model.Order).filter(model.Order.id == order_id).first()

def readOrder_byUser(db: Session, patient_id: int, skip: int = 0, limit: int = 100):
    return db.query(model.Order).filter(model.Order.patient_id == patient_id).offset(skip).limit(limit).all()

def readOrder_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Order).offset(skip).limit(limit).all()

def deleteOrder_all(db: Session):
    row_affected = db.query(model.Order).delete()
    db.commit()
    return row_affected
