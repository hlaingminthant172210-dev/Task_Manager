from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def generate_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=60)
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, "1234", algorithm="HS256")
    return encoded_jwt

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, "1234", algorithms=["HS256"])
        if payload.get("exp") and payload["exp"] >= datetime.now().timestamp():
            return payload
    except JWTError:
        return None
    
def get_current_user(token: str = Security(oauth2_scheme)):
    payload = decode_jwt_token(token)
    print("Decoded JWT payload:", payload)  # Debugging statement
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload