from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import Users, ShowUsers
from database import get_db
import models

router = APIRouter()

@router.get('/users',tags=['users'])
def find( db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users

# pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/users', response_model=ShowUsers,tags=['users'])
def create(request:Users, db: Session = Depends(get_db)):
    # hashedPassword = pwd_ctx.hash(request.password)
    new_user = models.Users(fname=request.fname,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/users/{id}', response_model=ShowUsers,tags=['users'])
def findOne(id:int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User {id} is not found!')
    return user