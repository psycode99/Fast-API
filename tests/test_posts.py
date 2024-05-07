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
