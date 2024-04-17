from random import random, randrange
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

my_posts = [{'title': 'Beaches in Florida', 'content': 'Check these awesome beaches now!', 'published': True, 'rating': 4, 'id':1},
             {'title': 'Beaches in California', 'content': 'Check these awesome beaches now!', 'published': True, 'rating': 4, 'id':2},
               {'title': 'Beaches in Spain', 'content': 'Check these awesome beaches now!', 'published': True, 'rating': 4, 'id':3}]


def get_p(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get('/')
async def root():
    return {"message":"Hello to my API !"}

@app.get('/posts')
def get_posts():
    return {"data":my_posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get('/posts/{id}')
def get_post(id: int):
    post = get_p(id=id)
    if not post:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"post with the id of {id} not found")
    return {"post": post}




@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = get_p(id=id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with the id of {id} not found")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post ):
    post_ = get_p(id=id)
    if not post_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with the id of {id} not found")
    
    post_["title"] = post.title
    post_["content"] = post.content
    post_['rating'] = post.rating
    
    return {"data": post_}