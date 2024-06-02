# Import local modules
from models import model
from services import *
from schemas import *
from schemas.Database import SessionLocal, engine # SQLite database handling


# Import python packages
from pydantic import BaseModel
from sqlalchemy.orm import Session # Session Handler
from os import path # Path handling

# FastAPI Stuffs
from fastapi import FastAPI # Base FastAPI class
from fastapi import Depends, Request, HTTPException # Request handling
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware # Middleware for token auth
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer # OAuth control package


# --- Preparation --- #

# DB Initiation
model.BaseDB.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Application initiation
app = FastAPI(title="API DigiSehat",
    description="API DigiSehat versi python",
    version="1.0.0",)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
blacklisted_tokens = set()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
# --- App Routing --- #

@app.get("/")
async def root():
    return {"message": "Success"}

# --- User Routes --- #

@app.post("/signup", response_model=UserSchema.User)
def createUser(user: UserSchema.UserCreate, db: Session = Depends(get_db)):
    user_exists = UserService.readUser_byUsername(db, username=user.username)
    if user_exists:
        raise HTTPException(status_code=400, detail="Username sudah digunakan")
    return UserService.createUser(db=db, user=user)


 
@app.post("/login") 
async def login(user: UserSchema.UserLogin, db: Session = Depends(get_db)):
    if not UserService.authenticate(db,user):
        raise HTTPException(status_code=400, detail="Username atau Password Salah!")

    user_login = UserService.readUser_byUsername(db,user.username)
    if user:
        access_token  = Auth.create_access_token(user.username)
        user_id = user_login.id
        user_role = user_login.role
        return {"user_id":user_id, "user_role":user_role, "access_token": access_token}
    else:
        raise HTTPException(status_code=400, detail=f"Tidak ada user dengan nama {user_id}")

@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    if token:
        blacklisted_tokens.add(token)
        return {"message": "Successfully logged out"}
    else:
        return {"message": "No token provided"}

@app.get("/user/{user_id}", response_model=UserSchema.User)
def readUser(user_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_user = UserService.readUser(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return db_user

@app.get("/users", response_model=list[UserSchema.User])
def readUser(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token) 
    db_users = UserService.readUser_all(db, skip=skip, limit=limit)
    if db_users is None:
        raise HTTPException(status_code=404, detail="List user kosong")
    return db_users

# --- Pasien Routes --- #

@app.post("/create_patient", response_model=PatientSchema.Patient)
def createPatient(patient: PatientSchema.PatientCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    patient_exists = PatientService.readPatient_byName(db, name=patient.name)
    if patient_exists:
        raise HTTPException(status_code=400, detail="Nama pasien sudah digunakan")
    return PatientService.createPatient(db=db, patient=patient)

@app.get("/patient/{patient_id}", response_model=PatientSchema.Patient)
def readPatient(patient_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_patient = PatientService.readPatient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Pasien tidak ditemukan")
    return db_patient

@app.get("/patientUID/{user_id}", response_model=PatientSchema.Patient)
def readPatient(user_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_patient = PatientService.readPatient_byUID(db, user_id=user_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Akun ini bukan akun pasien")
    return db_patient

@app.get("/patients", response_model=list[PatientSchema.Patient])
def readPatient(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token) 
    db_patient = PatientService.readPatient_all(db)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="List patient kosong")
    return db_patient

@app.get("/patients/searchName", response_model=list[PatientSchema.Patient])
def readPatient_nameAll(name: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token)
    db_patients = PatientService.readPatient_nameAll(db, name=name, skip=skip, limit=limit)
    if not db_patients:
        raise HTTPException(status_code=404, detail=f"Pasien {name} tidak ditemukan")
    return db_patients

# --- Doctor Routes --- #

@app.post("/create_doctor", response_model=DoctorSchema.Doctor)
def createDoctor(doctor: DoctorSchema.DoctorCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    doctor_exists = DoctorService.readDoctor_byName(db, name=doctor.name)
    if doctor_exists:
        raise HTTPException(status_code=400, detail="Nama dokter sudah digunakan")
    return DoctorService.createDoctor(db=db, doctor=doctor)

@app.get("/doctor/{doctor_id}", response_model=DoctorSchema.Doctor)
def readDoctor(doctor_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_doctor = DoctorService.readDoctor(db, doctor_id=doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Doctor tidak ditemukan")
    return db_doctor

@app.get("/doctorUID/{user_id}", response_model=DoctorSchema.Doctor)
def readDoctor_byUID(user_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_doctor = DoctorService.readDoctor_byUID(db, user_id=user_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="Akun ini bukan akun dokter")
    return db_doctor

@app.get("/doctors", response_model=list[DoctorSchema.Doctor])
def readDoctor_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token) 
    db_doctor = DoctorService.readDoctor_all(db)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="List doctor kosong")
    return db_doctor

@app.get("/doctors/searchName", response_model=list[DoctorSchema.Doctor])
def readDoctor_nameAll(name: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token)
    db_doctors = DoctorService.readDoctor_nameAll(db, name=name, skip=skip, limit=limit)
    if not db_doctors:
        raise HTTPException(status_code=404, detail=f"Dokter {name} tidak ditemukan")
    return db_doctors

@app.get("/doctors/searchSpecialty", response_model=list[DoctorSchema.Doctor])
def readDoctor_specialtyAll(specialty: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token)
    db_doctors = DoctorService.readDoctor_specialtyAll(db, specialty=specialty, skip=skip, limit=limit)
    if not db_doctors:
        raise HTTPException(status_code=404, detail=f"Dokter spesialis {specialty} tidak ditemukan")
    return db_doctors

# ---  Medicine Routes --- #

@app.post("/create_medicine", response_model=MedicineSchema.Medicine)
def createMedicine(medicine: MedicineSchema.MedicineCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    medicine_exists = MedicineService.readMedicine_byName(db, name=medicine.name)
    if medicine_exists:
        raise HTTPException(status_code=400, detail="Obat sudah ada")
    return MedicineService.createMedicine(db=db, medicine=medicine)

@app.get("/medicine/{medicine_id}", response_model=MedicineSchema.Medicine)
def readMedicine(medicine_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_medicine = MedicineService.readMedicine(db, medicine_id=medicine_id)
    if db_medicine is None:
        raise HTTPException(status_code=404, detail="Obat tidak ditemukan")
    return db_medicine

@app.get("/medicines", response_model=list[MedicineSchema.Medicine])
def readMedicine(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token) 
    db_medicine = MedicineService.readMedicine_all(db)
    if db_medicine is None:
        raise HTTPException(status_code=404, detail="List obat kosong")
    return db_medicine

# --- Diagnosis Routes --- #

@app.post("/create_diagnosis", response_model=DiagnosisSchema.Diagnosis)
def createDiagnosis(diagnosis: DiagnosisSchema.DiagnosisCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    return DiagnosisService.createDiagnosis(db=db, diagnosis=diagnosis)

@app.get("/diagnosis/{diagnosis_id}", response_model=DiagnosisSchema.Diagnosis)
def readDiagnosis(diagnosis_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_diagnosis = DiagnosisService.readDiagnosis(db, diagnosis_id=diagnosis_id)
    if db_diagnosis is None:
        raise HTTPException(status_code=404, detail="Diagnosis tidak ditemukan")
    return db_diagnosis

@app.get("/diagnosis_patient/{patient_id}", response_model=list[DiagnosisSchema.Diagnosis])
def readDiagnosis_byUser(patient_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100, token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_diagnosis = DiagnosisService.readDiagnosis_byUser(db, patient_id=patient_id)
    if db_diagnosis is None:
        raise HTTPException(status_code=404, detail="Pasien tidak memiliki diagnosis apa apa")
    return db_diagnosis

@app.get("/diagnoses", response_model=list[DiagnosisSchema.Diagnosis])
def readDiagnosis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token) 
    db_diagnosis = DiagnosisService.readDiagnosis_all(db)
    if db_diagnosis is None:
        raise HTTPException(status_code=404, detail="List diagnosis kosong")
    return db_diagnosis

# --- Illness Routes --- #

@app.post("/create_illness", response_model=IllnessSchema.Illness)
def createIllness(illness: IllnessSchema.IllnessCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    illness_exists = IllnessService.readIllness_byName(db, name=illness.name)
    if illness_exists:
        raise HTTPException(status_code=400, detail="Data penyakit sudah ada")
    return IllnessService.createIllness(db=db, illness=illness)

@app.get("/illness/{illness_id}", response_model=IllnessSchema.Illness)
def readIllness(illness_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_illness = IllnessService.readIllness(db, illness_id=illness_id)
    if db_illness is None:
        raise HTTPException(status_code=404, detail="Penyakit tidak ditemukan")
    return db_illness

@app.get("/illness_category/{category}", response_model=list[IllnessSchema.Illness])
def readIllness_byCategory(category: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 100, token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_illness = IllnessService.readIllness_byCategory(db, category=category)
    if db_illness is None:
        raise HTTPException(status_code=404, detail="Kategori penyakit {category} kosong")
    return db_illness

@app.get("/illnesses", response_model=list[IllnessSchema.Illness])
def readIllness_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token) 
    db_illness = IllnessService.readIllness_all(db)
    if db_illness is None:
        raise HTTPException(status_code=404, detail="List penyakit kosong")
    return db_illness

# --- Review Routes --- #

@app.post("/create_review", response_model=ReviewSchema.Review)
def createReview(review: ReviewSchema.ReviewCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    return ReviewService.createReview(db=db, review=review)

@app.get("/review/{review_id}", response_model=ReviewSchema.Review)
def readReview(review_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_review = ReviewService.readReview(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review tidak ditemukan")
    return db_review

@app.get("/review_patient/{patient_id}", response_model=list[ReviewSchema.Review])
def readReview_byUser(patient_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100, token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_review = ReviewService.readReview_byUser(db, patient_id=patient_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Pasien belum membuat review")
    return db_review

@app.get("/review_doctor/{doctor_id}", response_model=list[ReviewSchema.Review])
def readReview_byDoctor(doctor_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100, token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_review = ReviewService.readReview_byDoctor(db, doctor_id=doctor_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Dokter belum diberi review")
    return db_review

@app.get("/reviews", response_model=list[ReviewSchema.Review])
def readReview_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token) 
    db_review = ReviewService.readReview_all(db)
    if db_review is None:
        raise HTTPException(status_code=404, detail="List review kosong")
    return db_review

# --- Notification Route --- # 

@app.post("/create_notification", response_model=NotificationSchema.Notification)
def createNotification(notification: NotificationSchema.NotificationCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    # notification_exists = NotificationService.readNotification_byName(db, name=notification.name)
    # if notification_exists:
    #     raise HTTPException(status_code=400, detail="Obat sudah ada")
    return NotificationService.createNotification(db=db, notification=notification)

@app.get("/notification/{notification_id}", response_model=NotificationSchema.Notification)
def readNotification(notification_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_notification = NotificationService.readNotification(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notif tidak ditemukan")
    return db_notification

@app.get("/notification_patient/{patient_id}", response_model=list[NotificationSchema.Notification])
def readNotification_byUser(patient_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100, token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_notification = NotificationService.readNotification_byUser(db, patient_id=patient_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Tidak ada notif untuk pasien")
    return db_notification

@app.get("/notifications", response_model=list[NotificationSchema.Notification])
def readNotification_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token) 
    db_notification = NotificationService.readNotification_all(db)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Tidak ada notif untuk pasien")
    return db_notification

# --- Schedule Routes --- #
@app.post("/create_schedule", response_model=ScheduleSchema.Schedule)
def createSchedule(schedule: ScheduleSchema.ScheduleCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    return ScheduleService.createSchedule(db=db, schedule=schedule)

@app.get("/schedule/{schedule_id}", response_model=ScheduleSchema.Schedule)
def readSchedule(schedule_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token) 
    db_schedule = ScheduleService.readSchedule(db, schedule_id=schedule_id)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule tidak ditemukan")
    return db_schedule

@app.get("/schedule_patient/{patient_id}", response_model=list[ScheduleSchema.Schedule])
def readSchedule_byUser(patient_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100, token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token) 
    db_schedule = ScheduleService.readSchedule_byUser(db, patient_id=patient_id, skip=skip, limit=limit)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Pasien belum membuat janji dengan dokter")
    return db_schedule

@app.get("/schedule_doctor/{doctor_id}", response_model=list[ScheduleSchema.Schedule])
def readSchedule_byDoctor(doctor_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100, token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token) 
    db_schedule = ScheduleService.readSchedule_byDoctor(db, doctor_id=doctor_id, skip=skip, limit=limit)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Dokter tidak memiliki janji dengan pasien")
    return db_schedule

@app.get("/schedules", response_model=list[ScheduleSchema.Schedule])
def readSchedule_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token) 
    db_schedule = ScheduleService.readSchedule_all(db, skip=skip, limit=limit)
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Data schedule kosong")
    return db_schedule

# --- Order Routes --- #

@app.post("/create_order", response_model=OrderSchema.Order)
def createOrder(order: OrderSchema.OrderCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    return OrderService.createOrder(db=db, order=order)

@app.get("/order/{order_id}", response_model=OrderSchema.Order)
def readOrder(order_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_order = OrderService.readOrder(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order tidak ditemukan")
    return db_order

@app.get("/order_patient/{patient_id}", response_model=list[OrderSchema.Order])
def readOrder_byUser(patient_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100, token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_order = OrderService.readOrder_byUser(db, patient_id=patient_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Pasien belum memesan apa apa")
    return db_order

@app.get("/orders", response_model=list[OrderSchema.Order])
def readOrder_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token) 
    db_order = OrderService.readOrder_all(db)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Data order ksoong")
    return db_order

# --- Message Routes --- #

@app.post("/create_message", response_model=MessageSchema.Message)
def createMessage(message: MessageSchema.MessageCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    return MessageService.createMessage(db=db, message=message)

@app.get("/message/{message_id}", response_model=MessageSchema.Message)
def readMessage(message_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token)
    db_message = MessageService.readMessage(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message tidak ditemukan")
    return db_message

@app.get("/messages", response_model=list[MessageSchema.Message])
def readMessages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token)
    db_messages = MessageService.readMessage_all(db, skip=skip, limit=limit)
    return db_messages

# --- Hospital Routes --- #

@app.post("/create_hospital", response_model=HospitalSchema.Hospital)
def createHospital(hospital: HospitalSchema.HospitalCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    hospital_exists = HospitalService.readHospital_byName(db, name=hospital.name)
    if hospital_exists:
        raise HTTPException(status_code=400, detail="Rumah Sakit sudah ada")
    return HospitalService.createHospital(db=db, hospital=hospital)

@app.get("/hospital/{hospital_id}", response_model=HospitalSchema.Hospital)
def readHospital(hospital_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr =  Auth.verify_token(token) 
    db_hospital = HospitalService.readHospital(db, hospital_id=hospital_id)
    if db_hospital is None:
        raise HTTPException(status_code=404, detail="Rumah Sakit tidak ditemukan")
    return db_hospital

@app.get("/hospitals", response_model=list[HospitalSchema.Hospital])
def readHospital_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")
    usr = Auth.verify_token(token) 
    db_hospital = HospitalService.readHospital_all(db)
    if db_hospital is None:
        raise HTTPException(status_code=404, detail="List RS kosong")
    return db_hospital
  
@app.post("/token", response_model=Auth.Token)
async def token(req: Request, form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):

    f = UserService.UserCreate
    f.username = form_data.username
    f.password = form_data.password
    if not UserService.authenticate(db,f):
        raise HTTPException(status_code=400, detail="Username atau Password salah")

    username  = form_data.username
    access_token  = create_access_token(username)

    return {"access_token": access_token, "token_type": "bearer"}