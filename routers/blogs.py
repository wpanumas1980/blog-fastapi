from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas import Blogs, UpdateBlog, ShowBlogs, Users
from database import get_db
from oauth2 import get_current_user
from repository import blogs

router = APIRouter(
    prefix='/blogs',
    tags=['Blogs']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: Blogs, db: Session = Depends(get_db),current_user:Users = Depends(get_current_user)):
    return blogs.create(request,db)

@router.get('/',response_model=List[ShowBlogs])
def find( db: Session = Depends(get_db), current_user:Users = Depends(get_current_user)):
# def find( db: Session = Depends(get_db)):
    return blogs.find(db)

@router.get('/{id}', status_code=200,response_model=ShowBlogs,)
def findOne(id, db: Session = Depends(get_db),current_user:Users = Depends(get_current_user)):
    return blogs.findOne(id,db)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request: UpdateBlog, db: Session = Depends(get_db),current_user:Users = Depends(get_current_user)):
    return blogs.update(id,request,db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db: Session = Depends(get_db),current_user:Users = Depends(get_current_user)):
          return blogs.destroy(id,db)
