from schemas.Database import BaseDB
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from typing import List
from sqlalchemy import Table
from sqlalchemy import DateTime

class User(BaseDB):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    medical_record = Column(String, unique=True, index=True)
    nik = Column(String)
    gender = Column(String)
    address = Column(String)
    telephone = Column(String)
    date_of_birth = Column(String)
    allergy = Column(String)
    allergy_year = Column(String)

class Doctor(BaseDB):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    specialty = Column(String)
    hospital = Column(String)
    experience = Column(String)
    philosophy = Column(String)
    innovation = Column(String)

class Medicine(BaseDB):
    __tablename__ = "medicines"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    manufacturer = Column(String)
    dosage = Column(String)
    description = Column(String)
    instruction = Column(String)
    price = Column(Integer)

class Diagnosis(BaseDB):
    __tablename__ = "diagnosis"
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer)
    patient_id = Column(Integer)
    diagnosis_name = Column(String)
    recommendation = Column(String)
    medicine_recommendation = Column(String)

class Illness(BaseDB):
    __tablename__ = "illness"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    general_symptoms = Column(String)
    unique_symptoms = Column(String)
    extra_symptoms = Column(String)

class Review(BaseDB):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    doctor_id = Column(Integer)
    text = Column(String)
    date = Column(String)
    star = Column(Integer)


class Notification(BaseDB):
    __tablename__ = "notification"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    message = Column(String)

class Schedule(BaseDB):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    doctor_id = Column(Integer)
    reservation_num = Column(Integer)
    time = Column(String)
    location = Column(String)
    
class Order(BaseDB):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    medicine_id = Column(Integer)
    address = Column(String)
    courier = Column(String)
    payment = Column(String)


