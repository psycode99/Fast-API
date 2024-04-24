from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone
from . import schemas, database, models, config
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expires_in = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expires_in})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt    


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db) ):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                           headers={'WWW-Authenticate':"Bearer"} )
    
    verified_token = verify_access_token(token, credentials_exception=credentials_exception)
    user = db.query(models.User).filter_by(id=verified_token.id).first()

    return user
    
