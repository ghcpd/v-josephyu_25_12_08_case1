import os
import sqlite3
import tempfile

from app import app as flask_app
from models import init_db, get_connection, User


def setup_temp_app(tmp_path):
    dbfile = tmp_path / "test_models.db"
    flask_app.config['DATABASE'] = str(dbfile)
    flask_app.config['WTF_CSRF_ENABLED'] = False
    init_db(flask_app)
    return flask_app


def test_user_create_and_verify(tmp_path):
    app = setup_temp_app(tmp_path)
    conn = get_connection(app)
    u = User.create(conn, 'tester', 'secret-password', 'tester@example.com')
    assert u.username == 'tester'
    assert u.verify_password('secret-password') is True
    # persisted
    fetched = User.get_by_username(conn, 'tester')
    assert fetched is not None
    assert fetched.username == 'tester'
    conn.close()
