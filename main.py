from random import random, randrange
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

my_posts = [{'title': 'Beaches in Florida', 'content': 'Check these awesome beaches now!', 'published': True, 'rating': 4, 'id':1},
             {'title': 'Beaches in California', 'content': 'Check these awesome beaches now!', 'published': True, 'rating': 4, 'id':2},
               {'title': 'Beaches in Spain', 'content': 'Check these awesome beaches now!', 'published': True, 'rating': 4, 'id':3}]

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

@app.post('/posts')
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}



