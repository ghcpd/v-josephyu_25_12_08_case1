import os
import sys
import sqlite3
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, init_db


@pytest.fixture
def client(tmp_path):
    db_file = tmp_path / "test_db3.sqlite3"
    app.config['DATABASE'] = str(db_file)
    app.config['WTF_CSRF_ENABLED'] = False
    if db_file.exists():
        db_file.unlink()
    init_db(app)
    with app.test_client() as c:
        yield c


def test_short_password_rejected(client):
    rv = client.post('/register', data={'username':'shortpw','email':'s@example.com','password':'abc'}, follow_redirects=True)
    # Should not redirect to dashboard on short password
    assert b'Dashboard' not in rv.data


def test_missing_email_rejected(client):
    rv = client.post('/register', data={'username':'noemail','password':'password123'}, follow_redirects=True)
    assert b'Dashboard' not in rv.data
