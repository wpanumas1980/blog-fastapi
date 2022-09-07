
from fastapi import FastAPI,Depends,status,Request,Response,HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from schemas import Blogs

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blogs', status_code=status.HTTP_201_CREATED)
def create(request: Blogs, db: Session = Depends(get_db)):
    print('request =>', request)
    new_blog = models.Blogs(title=request.title,description=request.description)
    print('new_blog =>', new_blog)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@app.get('/blogs')
def find( db: Session = Depends(get_db)):
    blogs = db.query(models.Blogs).all()
    return blogs

@app.get('/blogs/{id}', status_code=200)
def findOne(id,response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id).first()
    if not blog:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} is not found!')

    return blog

@app.delete('/blogs/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db: Session = Depends(get_db)):
          blog = db.query(models.Blogs).filter(models.Blogs.id == id)
          if not blog.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} is not found!')
          blog.delete(synchronize_session=False)
          db.commit()
          return 'done'

@app.put('/blogs/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request: Blogs, db: Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog {id} is not found!')
    
    update_item_encoded = jsonable_encoder(request.dict(exclude_none=True))
    blog.update(update_item_encoded)
    db.commit()
    return 'updated'


#   print('update_item_encoded =>', update_item_encoded)