import datetime
from jose import JWTError, jwt
from datetime import timedelta

SECRET_KEY = "HJ62GkTz9&%y#s@LqE$pFD!v8*wN3^A7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expires_in = datetime.datetime.now() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expires_in})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt    
