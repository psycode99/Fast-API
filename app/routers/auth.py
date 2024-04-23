from fastapi import Depends, Response, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_db
from .. import models, utils, oauth2
from ..schemas import UserLogin

router = APIRouter(tags=['Authentication'])

@router.post('/login', status_code=status.HTTP_200_OK)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(get_db)):
    # using username instead of email cos that's how it is stored by default
    # in Oauth2PasswordRequestForm and when testing in Postman we'll be 
    # using form data to send the data rather than raw with JSON
    user = db.query(models.User).filter_by(email=user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    
    verify = utils.verify(user_credentials.password, user.password)
    if not verify:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Invalid Credentials")
    
    #create token
    access_token = oauth2.create_access_token({"user_id":user.id})

    #return token
    
    return {"access_token": access_token, "type":"bearer"}