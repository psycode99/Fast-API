from typing import List
from fastapi import Depends, FastAPI, HTTPException, Response, status
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import update
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .schemas import PostCreate, Post

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

@app.get('/')
def root():
    return {"message":"Hello to my API !"}


@app.get('/posts', response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    # cur.execute(""" SELECT * FROM "Post" """)
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    # cur.execute(f""" INSERT INTO "Post" (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #              vars=(post.title, post.content, post.published))
    # new_post = cur.fetchone()  
    # conn.commit() 

    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return  new_post


@app.get('/posts/{id}', response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cur.execute("""  SELECT * FROM "Post" WHERE id=%s """, vars=(str(id),))
    # post = cur.fetchone()
    post = db.query(models.Post).filter_by(id=id).first()
    if not post:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"post with the id of {id} not found")
    return  post




@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session =  Depends(get_db)):
    # cur.execute("""  DELETE FROM "Post" WHERE id=%s RETURNING * """, vars=(str(id),))
    # post = cur.fetchone()
    post = db.query(models.Post).filter_by(id=id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with the id of {id} not found")
    # conn.commit()
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}', status_code=status.HTTP_200_OK, response_model=Post)
def update_post(id: int, post: PostCreate,  db: Session = Depends(get_db)):
    # cur.execute("""  UPDATE "Post" SET title=%s, content=%s, published=%s WHERE id=%s  RETURNING * """,
    #             vars=(post.title, post.content, post.published, id))
    # post_ = cur.fetchone()
    to_be_updated_post = db.query(models.Post).filter_by(id=id).first()

    if not to_be_updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with the id of {id} not found")
    
    # maps columns of the specific post in the database with data 
    # from our pydantic model 
    stmt = (
        update(models.Post).
        where(models.Post.id == id).
        values(**post.model_dump())
        )
    
    db.execute(stmt)
    
    db.commit()
    # conn.commit()
  
    return to_be_updated_post