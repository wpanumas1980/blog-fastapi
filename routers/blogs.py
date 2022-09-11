from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import Blogs, UpdateBlog, ShowBlogs
from database import get_db
import models

router = APIRouter()

@router.get('/blogs',response_model=List[ShowBlogs],tags=['blogs'])
def find( db: Session = Depends(get_db)):
    blogs = db.query(models.Blogs).all()
    return blogs


@router.post('/blogs', status_code=status.HTTP_201_CREATED,tags=['blogs'])
def create(request: Blogs, db: Session = Depends(get_db)):
    new_blog = models.Blogs(title=request.title,description=request.description,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/blogs/{id}', status_code=200,response_model=ShowBlogs,tags=['blogs'])
def findOne(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id).first()
    if not blog:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} is not found!')
    return blog

@router.delete('/blogs/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def destroy(id,db: Session = Depends(get_db)):
          blog = db.query(models.Blogs).filter(models.Blogs.id == id)
          if not blog.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} is not found!')
          blog.delete(synchronize_session=False)
          db.commit()
          return 'done'

@router.put('/blogs/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update(id,request: UpdateBlog, db: Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} is not found!')
    update_item_encoded = jsonable_encoder(request.dict(exclude_unset=True))
    blog.update(update_item_encoded)
    db.commit()
    return 'updated'