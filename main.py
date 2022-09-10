from typing import List
from fastapi import FastAPI,Depends,status,Response,HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from schemas import Blogs, UpdateBlog, ShowBlogs, Users,ShowUsers
from hashing import Hash

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blogs', status_code=status.HTTP_201_CREATED,tags=['blogs'])
def create(request: Blogs, db: Session = Depends(get_db)):
    new_blog = models.Blogs(title=request.title,description=request.description,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@app.get('/blogs',response_model=List[ShowBlogs],tags=['blogs'])
def find( db: Session = Depends(get_db)):
    blogs = db.query(models.Blogs).all()
    return blogs

@app.get('/blogs/{id}', status_code=200,response_model=ShowBlogs,tags=['blogs'])
def findOne(id,response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id).first()
    if not blog:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} is not found!')
    return blog

@app.delete('/blogs/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def destroy(id,db: Session = Depends(get_db)):
          blog = db.query(models.Blogs).filter(models.Blogs.id == id)
          if not blog.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} is not found!')
          blog.delete(synchronize_session=False)
          db.commit()
          return 'done'

@app.put('/blogs/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update(id,request: UpdateBlog, db: Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} is not found!')
    
    # update_item_encoded = jsonable_encoder(request.dict(exclude_none=True))
    update_item_encoded = jsonable_encoder(request.dict(exclude_unset=True))
    blog.update(update_item_encoded)
    db.commit()
    return 'updated'

@app.get('/users',tags=['users'])
def find( db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users

# pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/users', response_model=ShowUsers,tags=['users'])
def create(request:Users, db: Session = Depends(get_db)):
    # hashedPassword = pwd_ctx.hash(request.password)
    new_user = models.Users(fname=request.fname,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users/{id}', response_model=ShowUsers,tags=['users'])
def findOne(id:int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User {id} is not found!')
    return user