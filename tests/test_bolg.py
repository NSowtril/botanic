import pytest
from botanic_website.db import get_db


def test_index(client, auth):
    response = client.get('/')
    assert b'Log in' in response.data
    assert b'Register' in response.data

    auth.login()
    response = client.get('/')
    assert b'Log out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-10-15' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize('path', (
    '/create',
    '1/update',
    '1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    #current user can't modify other user's post
    assert client.post('1/update').status_code == 403
    assert client.post('1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="1/update"' not in client.get('/').data


@pytest.mark.parametrize('path',(
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    
