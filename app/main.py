from typing import List
from fastapi import Depends, FastAPI, HTTPException, Response, status
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import update
from . import models, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .schemas import PostCreate, Post, UserCreate, UserResp
from .routers import posts, user

models.Base.metadata.create_all(bind=engine)
# creates the tables based on our predefined models in models.py


app = FastAPI()

while True:

    try:
        conn = psycopg2.connect(host='localhost',  database='fastapi', 
                                user='postgres', password='wordpress',
                                cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print('Database connection was successful!')
        break
    except Exception as err:
        print('Database connection failed')
        print(f"Error: {err}")


app.include_router(posts.router)
app.include_router(user.router)

@app.get('/')
def root():
    return {"message":"Hello to my API !"}



