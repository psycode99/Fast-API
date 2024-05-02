from fastapi import FastAPI
from . import models, config
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from .routers import posts, user, auth, vote

models.Base.metadata.create_all(bind=engine)
# creates the tables based on our predefined models in models.py
# commented out because we now have alembic to thank for migrations
# so we don't want it to be creating the tables before alembic does its thing -- migrations

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


settings = config.Settings()

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
    return {"message":"Hello to my API !"}



