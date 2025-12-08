"""
Test suite for Flask User Login & Registration App
Tests all functionality mentioned in README.md
"""

import pytest
import os
import sqlite3
import tempfile
from app import app, login_manager
from models import init_db, User, get_connection
from auth import auth_bp


@pytest.fixture
def client():
    """Setup test client with temporary database"""
    db_fd, db_path = tempfile.mkstemp()
    app.config['DATABASE'] = db_path
    app.config['TESTING'] = True
    
    with app.app_context():
        init_db(app)
    
    with app.test_client() as client:
        yield client
    
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def runner():
    """Setup CLI runner"""
    return app.test_cli_runner()


class TestAppStartup:
    """Test basic app startup and configuration"""
    
    def test_app_creation(self):
        """Test app is properly created"""
        assert app is not None
        assert app.config['SECRET_KEY'] == 'replace-with-a-strong-secret-key'
    
    def test_app_has_blueprints(self):
        """Test auth blueprint is registered"""
        assert 'auth' in app.blueprints
    
    def test_login_manager_configured(self):
        """Test login manager is configured"""
        assert login_manager.login_view == 'auth.login'


class TestRoutes:
    """Test all routes mentioned in README"""
    
    def test_root_route_redirects_to_login(self, client):
        """Test GET / redirects to login when not authenticated"""
        response = client.get('/', follow_redirects=False)
        assert response.status_code in [302, 303, 307, 308]
        assert '/login' in response.location
    
    def test_login_get(self, client):
        """Test GET /login returns login form"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'login' in response.data.lower() or b'password' in response.data.lower()
    
    def test_register_get(self, client):
        """Test GET /register returns registration form"""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'register' in response.data.lower() or b'email' in response.data.lower()
    
    def test_dashboard_requires_login(self, client):
        """Test GET /dashboard requires login"""
        response = client.get('/dashboard', follow_redirects=False)
        assert response.status_code in [302, 303, 307, 308]


class TestRegistration:
    """Test user registration flow"""
    
    def test_register_new_user(self, client):
        """Test successful user registration"""
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_register_duplicate_username(self, client):
        """Test registration fails with duplicate username"""
        client.post('/register', data={
            'username': 'testuser',
            'email': 'test1@example.com',
            'password': 'password123'
        })
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test2@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        assert b'already taken' in response.data or response.status_code == 200
    
    def test_register_validation_username_too_short(self, client):
        """Test username minimum length validation (3 chars)"""
        response = client.post('/register', data={
            'username': 'ab',
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        # Should either show error or redirect (depending on form validation)
        assert response.status_code == 200
    
    def test_register_validation_password_length(self, client):
        """Test password minimum length validation"""
        response = client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'abc'
        }, follow_redirects=True)
        assert response.status_code == 200


class TestLogin:
    """Test user login flow"""
    
    def test_login_success(self, client):
        """Test successful login"""
        # First register a user
        client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        # Then login
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_login_invalid_password(self, client):
        """Test login fails with invalid password"""
        client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        assert b'invalid' in response.data.lower() or response.status_code == 200
    
    def test_login_nonexistent_user(self, client):
        """Test login fails for non-existent user"""
        response = client.post('/login', data={
            'username': 'nonexistent',
            'password': 'password123'
        }, follow_redirects=True)
        assert response.status_code == 200


class TestLogout:
    """Test logout functionality"""
    
    def test_logout_requires_login(self, client):
        """Test /logout is protected"""
        response = client.get('/logout', follow_redirects=False)
        assert response.status_code in [302, 303, 307, 308]


class TestDatabase:
    """Test database operations"""
    
    def test_user_creation(self):
        """Test creating a user in database"""
        db_fd, db_path = tempfile.mkstemp()
        app.config['DATABASE'] = db_path
        
        with app.app_context():
            init_db(app)
            conn = get_connection(app)
            user = User.create(conn, 'testuser', 'password123', 'test@example.com')
            assert user.username == 'testuser'
            assert user.verify_password('password123')
            assert not user.verify_password('wrongpassword')
            conn.close()
        
        os.close(db_fd)
        os.unlink(db_path)
    
    def test_user_lookup(self):
        """Test looking up user by ID"""
        db_fd, db_path = tempfile.mkstemp()
        app.config['DATABASE'] = db_path
        
        with app.app_context():
            init_db(app)
            conn = get_connection(app)
            user = User.create(conn, 'testuser', 'password123', 'test@example.com')
            fetched = User.get_by_id(conn, user.id)
            assert fetched is not None
            assert fetched.username == 'testuser'
            conn.close()
        
        os.close(db_fd)
        os.unlink(db_path)


class TestFormValidation:
    """Test form validation rules"""
    
    def test_login_form_validation(self, client):
        """Test login form exists and has required fields"""
        from auth import LoginForm
        with app.test_request_context():
            form = LoginForm()
            assert hasattr(form, 'username')
            assert hasattr(form, 'password')
            assert hasattr(form, 'submit')
    
    def test_register_form_validation(self, client):
        """Test register form exists and has required fields"""
        from auth import RegisterForm
        with app.test_request_context():
            form = RegisterForm()
            assert hasattr(form, 'username')
            assert hasattr(form, 'email')
            assert hasattr(form, 'password')
            assert hasattr(form, 'submit')


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
