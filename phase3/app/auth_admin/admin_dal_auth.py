import motor.motor_asyncio
import os

async def check_token_logged_out(token_to_find):
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    db_connection = client.logged_out_tokens
    logged_out_tokens_collection = db_connection.get_collection("logged_out_tokens_coll")
        
    response = await logged_out_tokens_collection.find_one(
        {"access_token":token_to_find}
    )
    
    client.close()
    return response