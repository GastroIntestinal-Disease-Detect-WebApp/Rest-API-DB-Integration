from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas.patient_schemas import Patient, PatientInput
from dal.patient_collection_dal import get_all_patients_from_db,get_patient_by_id_from_db,add_patient_to_db


app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
def hello():
    return "Hey there"


@app.get("/patient/{id}",response_description="Get Existing Patient Details based on patient id",response_model=Patient,status_code=status.HTTP_200_OK)
async def get_patients_by_id(id: str) -> Patient:
    
    patient = await get_patient_by_id_from_db(id)
    if patient is not None:
        return patient
    else:
        raise HTTPException(status_code=404,detail=f"Patient with id = {id} does not exist")


@app.get("/patient",response_description="Get ALL Existing Patients Details",response_model=list[Patient],status_code=status.HTTP_200_OK)
async def get_all_patients() -> list[Patient]:
    
    patients = await get_all_patients_from_db()
    if patients is not None:
        return patients
    else:
        raise HTTPException(status_code=404,detail=f"Patients do not exist")


@app.post("/patient",response_description="Adding new patient",response_model=Patient,status_code=status.HTTP_201_CREATED)
async def add_patient(patientInputObject: PatientInput) -> Patient:
    
    created_patient = await add_patient_to_db(patientInputObject)
    # return created_student
    return created_patient


