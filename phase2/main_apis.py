from fastapi import FastAPI, status, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from schemas.patient_schemas import Patient, PatientInput, Image, Chat, InputSentMessage
from dal.patient_collection_dal import get_all_patients_from_db,get_patient_by_id_from_db,add_patient_to_db, add_patient_image_data_to_db, get_chats_for_a_particular_participant_from_db, get_chats_for_a_particular_participant_particular_chat_thread_from_db, add_chats_for_a_particular_chat_thread_into_db
from datetime import datetime

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


@app.post("/patient_image_data/{id}",response_description="Adding new Image",response_model=dict,status_code=status.HTTP_201_CREATED)
async def add_image_data(imageInputObject: Image, id: str) -> dict:
    
    # 1st checking if the patient exists:
    patient = await get_patient_by_id_from_db(id)
    if patient is not None:
        result_status = await add_patient_image_data_to_db(new_image=imageInputObject,patient_id=id)
        # return status of image data upload:
        return result_status
    else:
        return {"status":f"Patient with {id} does not exist"}

# get chat for a particular participant
@app.get("/chat/{participant_id}",response_model=list[Chat], status_code=status.HTTP_200_OK)
async def get_chats_for_a_particular_participant(participant_id: str) -> list[Chat]:
    chat = await get_chats_for_a_particular_participant_from_db(participant_id)
    return chat

# get chat for a particular participant's chat thread
@app.get("/chat_thread/{chat_thread_id}",response_model=Chat, status_code=status.HTTP_200_OK)
async def get_chats_for_a_particular_chat_thread(chat_thread_id: str) -> Chat:
    chat = await get_chats_for_a_particular_participant_particular_chat_thread_from_db(chat_thread_id)
    return chat

@app.post("/chat_thread/{chat_thread_id}",response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_chats_for_a_particular_chat_thread(chat_to_add : InputSentMessage, chat_thread_id: str):
    # get current date and time:
    current_data_and_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_data_and_time = str(current_data_and_time)
    
    # convert chat_to_add object into dictionary:
    chat_to_add_dict = chat_to_add.model_dump()
    
    # add the dateTime attribute to the dictionary:
    chat_to_add_dict["dateTime"] = current_data_and_time
        
    # add the dictionary to mongodb:
    status = await add_chats_for_a_particular_chat_thread_into_db(chat_to_add_dict, chat_thread_id)
    
    # return the status of operation:
    return status



@app.post("/dummy_test")
async def dummy_test(request: Request):
    some_dummy_data = await request.json()
    print(some_dummy_data)
    print(type(some_dummy_data))
    return some_dummy_data

