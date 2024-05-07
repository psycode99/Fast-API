import json
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app import models, schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.oauth2 import create_access_token

SQLACHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLACHEMY_DATABASE_URL, pool_pre_ping=True)

TestSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# sessionLocal serves as a factory for creating new sessions


@pytest.fixture(scope="function")
def session():
    """
    it deletes the previous tables when a new test is started
    creates the new database tables before our code is run
    and yields back a TestClient object
    
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    """
    this creates a new session via the TestSessionLocal
    and stores it in the db variable and then yields this db variable back.
    We can then use the new session via the db variable to query the database.
    """
    db = TestSessionLocal() 
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app=app)


@pytest.fixture
def test_user(client):
    user_data = {"email":"meeka@gmail.com", "password":"1234"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


# @pytest.fixture
# def create_test_posts(authorized_client):
#     new_post = authorized_client.post('/posts/', json={"title": "Best Hyper Cars in Europe", "content": "Porshe, Rimac, Bugatti"})
#     assert new_post.status_code == 201

#     return new_post

@pytest.fixture
def test_posts(test_user, session):
    post_data = [{
        "title": "Best Dog Breeds",
        "content": "huskies, Labradors and goldens",
        "owner_id": test_user['id']
    },
    {
        "title": "Best Cat Breeds",
        "content": "dunno not a cat person",
        "owner_id": test_user['id']
    },
    {
        "title": "Best Hyper Cars in Europe",
        "content": "Porshe, Rimac, Bugatti",
        "owner_id": test_user['id']
    }]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, post_data)

    session.add_all(list(post_map))
    session.commit()
    posts = session.query(models.Post).all()
    return posts