from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from hashing import Hash
from jwt import create_access_token
import models

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print('request =>', request)
    user = db.query(models.Users).filter(models.Users.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Invalid Credentials')
    if not Hash.verify(request.password , user.password):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Incorrect password')

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
