from fastapi import Depends, Response, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utils
from ..schemas import UserLogin

router = APIRouter(tags=['Authentication'])

@router.post('/login', status_code=status.HTTP_200_OK)
def login(user_credentials: UserLogin,  db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")
    
    verify = utils.verify(user_credentials.password, user.password)
    if not verify:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Invalid Credentials")
    
    #create token

    #return token
    
    return {"token": "token"}