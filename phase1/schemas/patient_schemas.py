from pydantic import BaseModel
from datetime import datetime

class Surgery(BaseModel):
    surgery_name: str
    surgery_date: str

class Image(BaseModel):
    image_link: str
    doctor_comment: str | None
    response_from_model: str | None = None

class CurrentMedication(BaseModel):
    medicine_name: str
    medicine_reason: str
    is_lifetime: bool
    medicine_frequency: str

class MedicalHistory(BaseModel):
    allergies: list[str] | None
    surgeries: list[Surgery] | None
    medication: list[CurrentMedication] | None


class PatientInput(BaseModel):
    first_name: str
    last_name: str
    birth_date: str
    address: str
    last_visit_date: str
    mobile_number: str
    email_id: str
    medical_history: MedicalHistory
    images: list[Image]
    blood_group: str
    gender: str

class Patient(PatientInput):
    id: str

