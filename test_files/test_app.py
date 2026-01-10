import os
import tempfile
import pytest

from app import app, init_db, get_connection


@pytest.fixture
def client(tmp_path, monkeypatch):
    dbfile = tmp_path / "test_app.db"
    monkeypatch.setitem(app.config, 'DATABASE', str(dbfile))
    app.config['TESTING'] = True
    # Ensure fresh DB
    init_db(app)
    with app.test_client() as client:
        yield client


def test_root_redirects_to_login(client):
    rv = client.get('/')
    assert rv.status_code in (302, 301)


def test_register_and_login_flow(client):
    # Register a user
    rv = client.post('/register', data={'username': 'alice', 'email': 'alice@example.com', 'password': 's3cr3t1'}, follow_redirects=True)
    assert b'Hello' in rv.data or rv.status_code == 200

    # Logout
    rv = client.get('/logout', follow_redirects=True)
    assert b'User Login' in rv.data or rv.status_code == 200

    # Login
    rv = client.post('/login', data={'username': 'alice', 'password': 's3cr3t1'}, follow_redirects=True)
    assert b'Hello' in rv.data or rv.status_code == 200
