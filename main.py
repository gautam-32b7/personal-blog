from fastapi import FastAPI

from routers import blogs, users, guests

from database import engine
from models import models

models.Base.metadata.create_all(bind=engine) # create tables

app = FastAPI()

app.include_router(users.router)
app.include_router(blogs.router)
app.include_router(guests.router)
