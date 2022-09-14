from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from schemas import Blogs
import models

def create(request: Blogs, db: Session):
    new_blog = models.Blogs(title=request.title,description=request.description,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def find( db: Session):
    blogs = db.query(models.Blogs).all()
    return blogs

def findOne(id, db: Session):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id).first()
    if not blog:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} is not found!')
    return blog

def update(id,request, db: Session):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} is not found!')
    update_item_encoded = jsonable_encoder(request.dict(exclude_unset=True))
    blog.update(update_item_encoded)
    db.commit()
    return 'updated'

def destroy(id:int,db: Session):
          blog = db.query(models.Blogs).filter(models.Blogs.id == id)
          if not blog.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} is not found!')
          blog.delete(synchronize_session=False)
          db.commit()
          return 'done'