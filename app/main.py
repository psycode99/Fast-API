from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
# creates the tables based on our predefined models in models.py

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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
async def root():
    return {"message":"Hello to my API !"}

@app.get('/sqlalchemy')
def test(db: Session = Depends(get_db)):
    return {"data": "success"}

@app.get('/posts')
def get_posts():
    cur.execute(""" SELECT * FROM "Post" """)
    posts = cur.fetchall()
    return {"data":posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cur.execute(f""" INSERT INTO "Post" (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                 vars=(post.title, post.content, post.published))
    new_post = cur.fetchone()  
    conn.commit() 
    return {"data": new_post}


@app.get('/posts/{id}')
def get_post(id: int):
    cur.execute("""  SELECT * FROM "Post" WHERE id=%s """, vars=(str(id),))
    post = cur.fetchone()
    if not post:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"post with the id of {id} not found")
    return {"post": post}




@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cur.execute("""  DELETE FROM "Post" WHERE id=%s RETURNING * """, vars=(str(id),))
    post = cur.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with the id of {id} not found")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post ):
    cur.execute("""  UPDATE "Post" SET title=%s, content=%s, published=%s WHERE id=%s  RETURNING * """,
                vars=(post.title, post.content, post.published, id))
    post_ = cur.fetchone()
    if not post_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with the id of {id} not found")
    
    conn.commit()
    
    return {"data": post_}