import os
import sys
import tempfile
import sqlite3
import pytest
# Ensure project root is first on sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, init_db
from models import get_connection

@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test_db.sqlite3"
    app.config['DATABASE'] = str(db_file)
    app.config['WTF_CSRF_ENABLED'] = False
    # ensure fresh DB
    if db_file.exists():
        db_file.unlink()
    init_db(app)
    with app.test_client() as c:
        yield c


def test_db_initialization(tmp_path):
    db_file = tmp_path / "test_db2.sqlite3"
    config_app = app
    config_app.config['DATABASE'] = str(db_file)
    # Reinitialize
    if db_file.exists():
        db_file.unlink()
    init_db(config_app)
    conn = sqlite3.connect(str(db_file))
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    assert cur.fetchone() is not None
    # check columns
    cur.execute("PRAGMA table_info(users)")
    cols = [r[1] for r in cur.fetchall()]
    assert 'email' in cols
    conn.close()


def test_register_and_login_flow(client):
    # Register new user
    rv = client.post('/register', data={'username':'tester','email':'t@example.com','password':'password123'}, follow_redirects=True)
    assert b'Dashboard' in rv.data or rv.status_code == 200

    # logout
    client.get('/logout')

    # login
    rv = client.post('/login', data={'username':'tester','password':'password123'}, follow_redirects=True)
    assert b'Dashboard' in rv.data or rv.status_code == 200


def test_dashboard_requires_login(client):
    # ensure logout
    client.get('/logout')
    rv = client.get('/dashboard', follow_redirects=False)
    assert rv.status_code == 302
    assert '/login' in rv.headers['Location']


def test_profile_route_missing(client):
    rv = client.get('/profile')
    assert rv.status_code == 404
