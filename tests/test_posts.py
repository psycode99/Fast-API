import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_post(client, test_posts):
    res = client.get('/posts/')
    assert res.status_code == 401
    

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get('/posts/999')
    assert res.status_code == 404


def test_get_one_valid_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostVote(**res.json())
    assert isinstance(post.Post.title, str)
    assert post.Post.id == test_posts[0].id
    assert res.status_code == 200


@pytest.mark.parametrize("title, content, is_published, status_code", [
    ("Best Hyper Cars in Europe", "Porshe, Rimac, Bugatti", True,  201),
    (12, None, True, 422),
    (12, 12, False, 422),
    (None, None, True, 422),
    ("Top EV brands", "tesla, rimac, ludicrous", False,  201)
    ])
def test_create_post(authorized_client, test_user, title, content, is_published, status_code):
    post_data = {"title": title, "content": content, "is_published":is_published}
    res = authorized_client.post('/posts', json=post_data)
    if res.status_code == 201:
        post = schemas.Post(**res.json())
        assert isinstance(post.title, str)
        assert isinstance(post.owner, schemas.UserResp)
        assert res.json().get('owner_id') == test_user['id']
    assert res.status_code == status_code


def test_unauthorized_create_post(client, test_user):
    post_data = {"title":"hello world", "content":"JS is cool",}
    res = client.post('/posts/', json=post_data)
    assert res.status_code == 401


    
    
