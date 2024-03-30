from fastapi import FastAPI, status, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from schemas.schemas import Patient, PatientInput, Image, Chat, InputSentMessage, CreateChatThreadInput, CreateChatThreadOutput
from dal.dal import get_all_patients_from_db,get_patient_by_id_from_db,add_patient_to_db, add_patient_image_data_to_db, get_chats_for_a_particular_participant_from_db, get_chats_for_a_particular_participant_particular_chat_thread_from_db, add_chats_for_a_particular_chat_thread_into_db, create_chat_thread_in_db, get_all_patients_under_doctor_supervision_from_db
from datetime import datetime
import uvicorn
from auth_admin.admin_get_payload_of_token import admin_get_payload_of_jwt_token
from auth_doctor.doctor_get_payload_of_token import doctor_get_payload_of_jwt_token
import requests


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


@app.get("/doctor_get_payload_of_jwt_token",response_description="Doctor: Return the payload of jwt token of doctor")
async def get_payload(payload_of_jwt_token: dict = Depends(doctor_get_payload_of_jwt_token, use_cache=False)) -> dict:
    return payload_of_jwt_token


@app.get("/verify_email_of_other_doctor/{email}",response_description="Doctor: route to verify whether the other doctor exists or not")
async def verify_doctor_email(email: str, payload_of_jwt_token: dict = Depends(doctor_get_payload_of_jwt_token, use_cache=False)) -> dict:
    
    print("Hello")
    
    api_url = f"http://127.0.0.1:8002/verify_email/{email}"
    
    response = requests.get(api_url).json()
    
    if response["message"] == "User Does Not Exist":
        return {"message": "User Does Not Exist"}

    elif response["message"] == "User Exists":
        return {"message": "User Exists"}

@app.get("/patient/{id}",response_description="Admin : Get Existing Patient Details based on patient id",response_model=Patient,status_code=status.HTTP_200_OK)
async def get_patients_by_id(id: str, payload_of_jwt_token: dict = Depends(admin_get_payload_of_jwt_token, use_cache=False)) -> Patient:
    
    patient = await get_patient_by_id_from_db(id)
    if patient is not None:
        return patient
    else:
        raise HTTPException(status_code=404,detail=f"Patient with id = {id} does not exist")


@app.get("/patient",response_description="Admin : Get ALL Existing Patients Details",response_model=list[Patient],status_code=status.HTTP_200_OK)
async def get_all_patients(payload_of_jwt_token: dict = Depends(admin_get_payload_of_jwt_token, use_cache=False)) -> list[Patient]:
    
    patients = await get_all_patients_from_db()
    if patients is not None:
        return patients
    else:
        raise HTTPException(status_code=404,detail=f"Patients do not exist")


@app.post("/patient",response_description="Admin: Adding new patient",response_model=Patient,status_code=status.HTTP_201_CREATED)
async def add_patient(patientInputObject: PatientInput, payload_of_jwt_token: dict = Depends(admin_get_payload_of_jwt_token, use_cache=False)):
    print(patientInputObject)
    created_patient = await add_patient_to_db(patientInputObject)
    return created_patient


@app.get("/patients_under_supervision",response_description="Doctor : Get ALL Patients Details which are under the supervision of that doctor",response_model=list[Patient],status_code=status.HTTP_200_OK)
async def get_all_patients(payload_of_jwt_token: dict = Depends(doctor_get_payload_of_jwt_token, use_cache=False)) -> list[Patient]:
    
    doctor_email = payload_of_jwt_token["email"]
    
    patients = await get_all_patients_under_doctor_supervision_from_db(doctor_email)
    
    if patients is not None:
        return patients
    else:
        raise HTTPException(status_code=404,detail=f"Patients do not exist")

# this api will take the json object to insert into db and will check if the patient exists and will also check if the doctor is authorised to add any data of this patient.
@app.post("/patient_image_data/{id}",response_description="Doctor: Adding new Image of patient by authorised doctor",response_model=dict,status_code=status.HTTP_201_CREATED)
async def add_image_data(imageInputObject: Image, id: str, payload_of_jwt_token: dict = Depends(doctor_get_payload_of_jwt_token, use_cache=False)) -> dict:
    
    doctor_email = payload_of_jwt_token["email"]
    
    patients = await get_all_patients_under_doctor_supervision_from_db(doctor_email)
    
    flag = 0
    for patient in patients:
        if patient["id"] == id:
            flag = 1
            break
    
    if flag == 0:
        raise HTTPException(status_code=401, detail="You don't have permission to access this patient's profile OR this patient with given ID does not exist")
    
    result_status = await add_patient_image_data_to_db(new_image=imageInputObject,patient_id=id)
    # return status of image data upload:
    return result_status

# get chat for a particular participant
@app.get("/chat/{participant_id}",response_model=list[Chat], status_code=status.HTTP_200_OK,response_description="Doctor: Get chat overview for a particular valid doctor email")
async def get_chats_for_a_particular_participant(participant_id: str,payload_of_jwt_token: dict = Depends(doctor_get_payload_of_jwt_token, use_cache=False)) -> list[Chat]:
    chat = await get_chats_for_a_particular_participant_from_db(participant_id)
    return chat

# get chat for a particular participant's chat thread
@app.get("/chat_thread/{chat_thread_id}",response_model=Chat, status_code=status.HTTP_200_OK, response_description="Doctor : Get all the chats of a chat thread (for a particular doctor conversation) but validate authorisation using token verification")
async def get_chats_for_a_particular_chat_thread(chat_thread_id: str,payload_of_jwt_token: dict = Depends(doctor_get_payload_of_jwt_token, use_cache=False)) -> Chat:
    chat = await get_chats_for_a_particular_participant_particular_chat_thread_from_db(chat_thread_id)
    return chat

@app.post("/chat_thread/{chat_thread_id}",response_model=dict, status_code=status.HTTP_201_CREATED,response_description="Doctor: Send message to other doctor by Adding a chat to the db")
async def add_chats_for_a_particular_chat_thread(chat_to_add : InputSentMessage, chat_thread_id: str, payload_of_jwt_token: dict = Depends(doctor_get_payload_of_jwt_token, use_cache=False)):
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

@app.post("/create_chat_thread",response_model=CreateChatThreadOutput,response_description="Doctor: Create a new chat thread of doctor with another doctor")
async def create_chat_thread(NewChatThread: CreateChatThreadInput,payload_of_jwt_token: dict = Depends(doctor_get_payload_of_jwt_token, use_cache=False)):
    # create chat_thread_id
    current_data_and_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    current_data_and_time = str(current_data_and_time)
    chat_thread_id = str(NewChatThread.participants[0]) + "-" + str(NewChatThread.participants[1]) + "-" + current_data_and_time
    
    # get dictionary representation of object
    chat_dict_to_insert = NewChatThread.model_dump()
    
    # add the fields to dictionary
    chat_dict_to_insert["chat_thread_id"] = chat_thread_id
    chat_dict_to_insert["chats"] = []
    
    # add the dictionary to mongodb
    created_chat_object = await create_chat_thread_in_db(chat_dict_to_insert)
    
    print(created_chat_object)
    print(type(created_chat_object))
    
    # return the newly created chat object
    return created_chat_object

@app.post("/dummy_test")
async def dummy_test(request: Request):
    some_dummy_data = await request.json()
    print(some_dummy_data)
    print(type(some_dummy_data))
    return some_dummy_data

if __name__ == "__main__":
    uvicorn.run("main_apis:app",reload=True,port=8000)