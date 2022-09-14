from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import Users, ShowUsers
from database import get_db

from repository import users

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', response_model=ShowUsers)
def create(request:Users, db: Session = Depends(get_db)):
    return users.create(request,db)

@router.get('/')
def find( db: Session = Depends(get_db)):
    return users.find(db)

@router.get('/{id}', response_model=ShowUsers)
def findOne(id:int, db: Session = Depends(get_db)):
    return users.findOne(id,db)