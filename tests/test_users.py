from app import schemas
import pytest
from jose import jwt
from app.oauth2 import SECRET_KEY, ALGORITHM
from fastapi import HTTPException

from tests.conftest import test_user


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


@pytest.mark.parametrize("email, password, status_code", [
    ("meeka@gmail.com", "ddd", 403),
    ("mike@gmail.com", "1234", 403),
    ('mike@gmail.com',  "gggg", 403) ,
    (None, "1234", 422),
    ("meeka@gmail.com", None, 422)
    ])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post('/login', data={"username":email, "password":password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == detail