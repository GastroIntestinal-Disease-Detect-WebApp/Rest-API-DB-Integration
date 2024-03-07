import motor.motor_asyncio
import os


def _get_mp_db_connection():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db_connection = client.mp_db
    return db_connection,client



def get_patient_collection():
    # in real world the connection with db is not a part of the main_apis.py file
    db_conn,client = _get_mp_db_connection()
    patient_collection = db_conn.get_collection("patient")
    return patient_collection