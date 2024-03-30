import motor.motor_asyncio
import os
from schemas.schemas import Patient,PatientInput, Image, Chat
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
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db_connection = client.mp_db
    patient_collection = db_connection.get_collection("patient")
    
    cursor = patient_collection.find()
    patients = await cursor.to_list(length=None)  # Retrieve all documents without limit
    
    client.close()
    return patients

async def get_all_patients_under_doctor_supervision_from_db(doctor_email: str) -> list[Patient]:
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db_connection = client.mp_db
    patient_collection = db_connection.get_collection("patient")
    
    cursor = patient_collection.find({"doctor_assigned": doctor_email})
    patients = await cursor.to_list(length=None)  # Retrieve all documents without limit
    
    client.close()
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

# this method adds the patient image data to db, not the image !
async def add_patient_image_data_to_db(new_image: Image, patient_id: str) -> dict:
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db_connection = client.mp_db
    patient_collection = db_connection.get_collection("patient")
    
    image_dict_to_insert = new_image.model_dump()
    
    result = await patient_collection.update_one(
        {"id": patient_id},
        {"$push": {"images": image_dict_to_insert}}
    )
    
    # print(result)
    # print(result.modified_count)
    
    client.close()
    
    if result.modified_count:
        return {"detail": "Image added successfully"}
    else:
        return {"detail": "Update failed"}

async def get_chats_for_a_particular_participant_from_db(participant_id: str) -> list[Chat]:
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db_connection = client.mp_db
    chat_collection = db_connection.get_collection("chat_coll")
    cursor = chat_collection.find({"participants": participant_id})
    chat = await cursor.to_list(length=None)
    client.close()
    return chat

async def get_chats_for_a_particular_participant_particular_chat_thread_from_db(chat_thread_id: str) -> Chat:
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db_connection = client.mp_db
    chat_collection = db_connection.get_collection("chat_coll")
    chat = await chat_collection.find_one({"chat_thread_id": chat_thread_id})
    client.close()
    return chat

async def add_chats_for_a_particular_chat_thread_into_db(chat_to_add_dict: dict, chat_thread_id: str):
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db_connection = client.mp_db
    chat_collection = db_connection.get_collection("chat_coll")
    
    update_result = await chat_collection.update_one(
    {"chat_thread_id": chat_thread_id},
    {
        "$push": {
            "chats": chat_to_add_dict
        }
    }
    )
    
    client.close()
    print(update_result)
    print(update_result.modified_count)
    
    if update_result.modified_count == 0:
        return {"status": "Chat message adding failed"}
    
    return {"status": "Chat message added successfully."}


async def create_chat_thread_in_db(chat_dict_to_insert: dict):
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db_connection = client.mp_db
    chat_collection = db_connection.get_collection("chat_coll")
    
    print(chat_dict_to_insert)
    
    
    new_chat = await chat_collection.insert_one(chat_dict_to_insert)
    
    client.close()
    
    created_chat = await get_chats_for_a_particular_participant_particular_chat_thread_from_db(chat_dict_to_insert["chat_thread_id"])
    print(created_chat)
    return created_chat
    
