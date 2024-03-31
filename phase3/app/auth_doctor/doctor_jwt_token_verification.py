import jwt
from cryptography.hazmat.primitives import serialization
from auth_doctor.doctor_dal_auth import check_token_logged_out

async def verify_token(token, public_key):
    try:
        header_data = jwt.get_unverified_header(token)
    except:
        return {"message": "Invalid Token"}

    key = serialization.load_ssh_public_key(public_key.encode())

    # verify token:
    try:
        payload_of_decoded_token = jwt.decode(jwt=token, key=key, algorithms=[header_data['alg']])

    except jwt.exceptions.InvalidSignatureError:
        return {"message": "Invalid Token"}

    except jwt.exceptions.ExpiredSignatureError:
        return {"message": "Token has Expired"}

    response = await check_token_logged_out(token)
    
    # if the token has been logged out : 
    if response is not None:
        return {"message":"Token has been Logged Out"}
    
    
    # checking if the token's payload contains: user_type = admin
    if(payload_of_decoded_token["user_type"] == "doctor"):
        payload_of_decoded_token["message"] = "Valid Token"
        return payload_of_decoded_token 
    
    else:
        return {"message":"Token is valid but of incorrect user type"}
    
        
    
        
    
