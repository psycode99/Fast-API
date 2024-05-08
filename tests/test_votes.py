def test_vote_on_post(authorized_client, test_posts, test_user):
    res = authorized_client.post('/votes/', json={"post_id": test_posts[3].id, 'dir':1})
    assert  res.status_code == 201


def test_vote_on_already_voted_post(authorized_client, test_posts, vote_on_post):
    res = authorized_client.post('/votes/', json={"post_id": test_posts[3].id, 'dir':1})
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts, vote_on_post):
    res = authorized_client.post('/votes/', json={'post_id': test_posts[3].id, 'dir':0})
    assert res.json().get('Message') == 'Successfully deleted vote'
    assert res.status_code == 201


def test_delete_non_existent_vote(authorized_client, test_posts):
    res = authorized_client.post('/votes/', json={'post_id':test_posts[0].id, 'dir':0})
    assert res.status_code == 404


def test_vote_on_non_existent_post(authorized_client):
    res = authorized_client.post('/votes/', json={'post_id':2000, 'dir':1})
    assert res.status_code == 404


def test_unauthorized_user_vote(client, test_posts):
    res = client.post('/votes/', json={"post_id": test_posts[3].id, 'dir':1})
    res.status_code == 401