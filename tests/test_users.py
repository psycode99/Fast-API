from app import schemas
from .database import client, session
import pytest
from jose import jwt
from app.oauth2 import SECRET_KEY, ALGORITHM


@pytest.fixture
def test_user(client):
    user_data = {"email":"meeka@gmail.com", "password":"1234"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


def test_root(client):
    res = client.get('/')
    assert res.json().get("message") == "Hello World!!!"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post('/users/', json={"email":"meeka@gmail.com", "password":"1234"})
    new_user = schemas.UserResp(**res.json())
    assert new_user.email == "meeka@gmail.com"
    assert res.status_code == 201


def test_login(client, test_user):
    res = client.post('/login', data={"username":test_user['email'], "password":test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    id: str = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200