from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from schemas import Users
from hashing import Hash
import models

def create(request:Users, db: Session):
    # hashedPassword = pwd_ctx.hash(request.password)
    new_user = models.Users(fname=request.fname,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def find( db: Session):
    users = db.query(models.Users).all()
    return users

def findOne(id, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User {id} is not found!')
    return user