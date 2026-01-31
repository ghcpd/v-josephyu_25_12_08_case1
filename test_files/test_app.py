import pytest

from app import app as flask_app
from models import init_db, get_connection


@pytest.fixture
def client(tmp_path):
    dbfile = tmp_path / "test_app.db"
    flask_app.config['DATABASE'] = str(dbfile)
    flask_app.config['TESTING'] = True
    # disable CSRF for testing forms
    flask_app.config['WTF_CSRF_ENABLED'] = False
    init_db(flask_app)

    with flask_app.test_client() as client:
        yield client


def test_register_and_dashboard_flow(client):
    # register should redirect to dashboard on success
    resp = client.post('/register', data={'username': 'alice', 'email': 'alice@example.com', 'password': 's3cret'}, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Hello, <strong>alice</strong>' in resp.data

    # logout
    client.get('/logout', follow_redirects=True)

    # login with correct credentials
    resp2 = client.post('/login', data={'username': 'alice', 'password': 's3cret'}, follow_redirects=True)
    assert resp2.status_code == 200
    assert b'Hello, <strong>alice</strong>' in resp2.data


def test_dashboard_requires_login(client):
    # when not logged in, dashboard should redirect to login
    resp = client.get('/dashboard', follow_redirects=False)
    assert resp.status_code in (302, 301)
    assert '/login' in resp.headers.get('Location', '')


def test_duplicate_registration(client):
    r1 = client.post('/register', data={'username': 'bob', 'email': 'bob@example.com', 'password': 'password123'}, follow_redirects=True)
    assert r1.status_code == 200
    # Attempt to register same username again
    r2 = client.post('/register', data={'username': 'bob', 'email': 'bob2@example.com', 'password': 'password123'}, follow_redirects=True)
    assert b'Username is already taken' in r2.data
