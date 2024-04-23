from fastapi import status, Depends, HTTPException, Response, APIRouter
from .. import models
from typing import List
from ..schemas import Post, PostCreate
from..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import update

router = APIRouter(
    prefix='/posts'
)

@router.get('/', response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    # cur.execute(""" SELECT * FROM "Post" """)
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Post)
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


@router.get('/{id}', response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cur.execute("""  SELECT * FROM "Post" WHERE id=%s """, vars=(str(id),))
    # post = cur.fetchone()
    post = db.query(models.Post).filter_by(id=id).first()
    if not post:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"post with the id of {id} not found")
    return  post




@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
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

@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=Post)
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