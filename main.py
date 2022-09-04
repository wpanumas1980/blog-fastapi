
from fastapi import FastAPI,Depends
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

@app.post('/blogs')
def create(request: Blogs, db: Session = Depends(get_db)):
    new_blog = models.Blogs(title=request.title,description=request.description)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@app.get('/blogs')
def find( db: Session = Depends(get_db)):
    blogs = db.query(models.Blogs).all()
    return blogs

@app.get('/blogs/{id}')
def findOne(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blogs).filter(models.Blogs.id == id).first()
    return blog