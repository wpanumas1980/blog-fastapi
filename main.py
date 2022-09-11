from fastapi import FastAPI
from database import engine
from routers import blogs, users
import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(blogs.router)
app.include_router(users.router)
