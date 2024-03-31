from fastapi import Header,HTTPException
from auth_admin.admin_jwt_token_verification import verify_token
from auth_admin.admin_singleton_pub_key import ClassicSingleton


async def admin_get_payload_of_jwt_token(authorization: str = Header(None)):
    
    singleton_object = ClassicSingleton()
    
    public_key = singleton_object.get_data()
    
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        scheme, token = authorization.split()
        
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail="Invalid token type")
        
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    response = await verify_token(token, public_key)
    
    if response["message"] == "Invalid Token":
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    elif response["message"] == "Token has Expired":
        raise HTTPException(status_code=401, detail="Token has Expired")

    elif response["message"] == "Token has been Logged Out":
        raise HTTPException(status_code=401, detail="Token has been Logged Out")
    
    elif response["message"] == "Token is valid but of incorrect user type":
        raise HTTPException(status_code=401, detail="Token is valid but of incorrect user type")
    
    return response  