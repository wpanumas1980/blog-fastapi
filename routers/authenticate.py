from fastapi import APIRouter, Depends, HTTPException, status
from schemas import Login
from sqlalchemy.orm import Session
from database import get_db
from hashing import Hash
import models

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(request:Login, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Invalid Credentials')
    if Hash.verify(request.password , user.password):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Incorrect password')
    return user