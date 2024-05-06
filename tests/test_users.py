from fastapi.testclient import TestClient
import pytest
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base

SQLACHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLACHEMY_DATABASE_URL, pool_pre_ping=True)

TestSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# sessionLocal serves as a factory for creating new sessions


@pytest.fixture
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


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app=app)
    

def test_root(client):
    res = client.get('/')
    assert res.json().get("message") == "Hello World!!!"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post('/users/', json={"email":"meeka@gmail.com", "password":"1234"})
    new_user = schemas.UserResp(**res.json())
    assert new_user.email == "meeka@gmail.com"
    assert res.status_code == 201