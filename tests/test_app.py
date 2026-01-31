import os
import sys
import pathlib
import tempfile
import pytest
# Ensure project root is on sys.path for pytest imports
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app, init_db
from models import get_connection

@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a temporary database for tests
    db_file = tmp_path / "test.db"
    monkeypatch.setitem(app.config, 'DATABASE', str(db_file))

    # Re-init db
    init_db(app)

    with app.test_client() as client:
        yield client


def test_index_redirects_to_login(client):
    rv = client.get('/')
    assert rv.status_code in (302, 301)
    assert '/login' in rv.location


def get_csrf_from(html_bytes):
    import re
    m = re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', html_bytes.decode('utf-8'))
    return m.group(1) if m else None


def test_register_requires_email_and_min_password(client):
    # Missing email (README says optional) should fail because form requires it
    # First GET the register form to obtain CSRF token
    get = client.get('/register')
    csrf = get_csrf_from(get.data)
    rv = client.post('/register', data={'username': 'u1', 'password': 'pass123', 'csrf_token': csrf}, follow_redirects=True)
    assert b'This field is required' in rv.data or b'Email' in rv.data

    # Short passwords (length 3) should fail because form enforces min 6
    get2 = client.get('/register')
    csrf2 = get_csrf_from(get2.data)
    rv2 = client.post('/register', data={'username': 'u2', 'password': '123', 'email': 'a@b.com', 'csrf_token': csrf2}, follow_redirects=True)
    assert b'Field must be between' in rv2.data or b'Field must be at least' in rv2.data


def test_register_and_login_flow(client):
    # Register a new user
    get = client.get('/register')
    csrf = get_csrf_from(get.data)
    rv = client.post('/register', data={'username': 'tester', 'password': 'safepass', 'email': 't@example.com', 'csrf_token': csrf}, follow_redirects=True)
    # After successful register, should reach dashboard
    assert b'You are logged in' in rv.data

    # Logout
    rv2 = client.get('/logout', follow_redirects=True)
    assert b'User Login' in rv2.data

    # Login (need to get csrf token for login form)
    get_login = client.get('/login')
    csrf_login = get_csrf_from(get_login.data)
    rv3 = client.post('/login', data={'username': 'tester', 'password': 'safepass', 'csrf_token': csrf_login}, follow_redirects=True)
    assert b'You are logged in' in rv3.data


def test_database_location_and_init(client, tmp_path):
    # Check that the configured DATABASE file exists and is the expected app db path
    db_path = app.config.get('DATABASE')
    assert os.path.exists(db_path)
    # Ensure the users table exists
    conn = get_connection(app)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    row = cur.fetchone()
    conn.close()
    assert row is not None
