from fastapi import FastAPI, status, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from schemas.patient_schemas import Patient, PatientInput
from dal.patient_collection_dal import get_patient_collection
from datetime import datetime

app = FastAPI()

patient_collection = get_patient_collection()

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

@app.post("/patient",response_description="Adding new patient",response_model=Patient,status_code=status.HTTP_201_CREATED)
async def add_patient(patientInputObject: PatientInput):
    now = datetime.now()
    # hour, minute, second, microsecond:
    current_time = now.strftime("%H%M%S%f")
    random_id = patientInputObject.first_name + "-" + patientInputObject.last_name + "-" + current_time 
    
    # doubt:mystry why the below line gave error:
    # patientObject = Patient.model_validate(patientInputObject)
    
    # converting the patientInputObject into a python dictionary: 
    patient_data = patientInputObject.model_dump()
    
    # adding id to the dictionary:
    patient_data['id'] = random_id
    
    new_patient = await patient_collection.insert_one(
        patient_data
    )
    
    created_patient = await patient_collection.find_one(
        {"id":patient_data['id']}
    )
    
    # return created_student
    return created_patient

@app.get("/patient/{id}",response_description="Get Existing Patient Details based on patient id",response_model=Patient,status_code=status.HTTP_200_OK)
async def get_all_patients(id: str):
    patient = await patient_collection.find_one(
        {"id":id}
    )
    if patient is not None:
        return patient
    else:
        raise HTTPException(status_code=404,detail=f"Patient with id = {id} does not exist")


@app.get("/patient",response_description="Get ALL Existing Patients Details",response_model=list[Patient],status_code=status.HTTP_200_OK)
async def get_all_patients():
    cursor = patient_collection.find()
    patients = await cursor.to_list(length=None)  # Retrieve all documents without limit
    if patients is not None:
        return patients
    else:
        raise HTTPException(status_code=404,detail=f"Patients do not exist")
    

# if __name__ == "__main__":
#     uvicorn.run("main_apis:app",reload=True,port=8000)