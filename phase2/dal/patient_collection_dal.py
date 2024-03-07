import motor.motor_asyncio
import os
from schemas.patient_schemas import Patient,PatientInput
from datetime import datetime


async def get_patient_by_id_from_db(id:str) -> Patient | None :
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db_connection = client.mp_db
    patient_collection = db_connection.get_collection("patient")
    
    patient = await patient_collection.find_one(
        {"id":id}
    )
    
    client.close()
    return patient


async def get_all_patients_from_db() -> list[Patient] :
    print("FLAGGING2")
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db_connection = client.mp_db
    patient_collection = db_connection.get_collection("patient")
    print("FLAGGING3")
    cursor = patient_collection.find()
    patients = await cursor.to_list(length=None)  # Retrieve all documents without limit
    print("FLAGGING4")
    client.close()
    print("FLAGGING5")
    print(type(patients))
    return patients


async def add_patient_to_db(patientInputObject:PatientInput) -> Patient:
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db_connection = client.mp_db
    patient_collection = db_connection.get_collection("patient")
    
    now = datetime.now()
    current_time = now.strftime("%H%M%S%f")
    random_id = patientInputObject.first_name + "-" + patientInputObject.last_name + "-" + current_time 
    
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
    
    client.close()
    return created_patient


