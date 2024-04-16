from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get('/')
async def root():
    return {"message":"Hello to my API !"}

@app.get('/posts')
def get_posts():
    return {"data":"new post"}

@app.post('/createpost')
def create_post(payLoad: dict = Body(...)):
    print(payLoad)
    return {"new_post": f"title: {payLoad['title']}, content: {payLoad['content']}"}



