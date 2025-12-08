# Flask User Login & Registration App

This project is a simple Flask-based user registration and login example. It includes:

- User registration, login, and logout
- A login-protected dashboard page at `/dashboard`
- A local SQLite database file `app.db`
- Session management via Flask-Login

This README describes the current implementation of the app based on the existing code in `app.py`, `auth.py`, and `models.py`.


---

## 1. Requirements

- Python 3.10+ (examples below use Windows PowerShell)
- `pip` installed
- Recommended: a virtual environment to isolate dependencies

---

## 2. Project Structure

```text
.
├─ app.py               # App entrypoint, blueprints, login config, Flask startup
├─ auth.py              # Auth blueprint: register, login, logout
├─ models.py            # Database models and initialization logic
├─ templates/
│  ├─ base.html         # Base layout
│  ├─ login.html        # Login page
│  ├─ register.html     # Registration page
│  └─ dashboard.html    # Dashboard page after login
├─ requirements.txt     # Python dependencies
├─ test_app.py          # Pytest test suite
├─ setup.ps1            # Setup script for Windows PowerShell
├─ setup.sh             # Setup script for Bash/Linux
├─ run_tests.ps1        # Test runner for Windows PowerShell
├─ run_tests.sh         # Test runner for Bash/Linux
└─ README.md            # This documentation
```

---

## 3. Installation & Run

The following commands assume Windows PowerShell. First, change to the project directory

### 3.1 Create and Activate Virtual Environment (Windows PowerShell)

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

### 3.2 Install Dependencies

Preferred: use `requirements.txt`:

```powershell
pip install -r requirements.txt
```

For quick testing, you may also directly install the core packages (reference only):

```powershell
pip install flask flask-login flask-wtf wtforms email_validator pytest
```

### 3.3 Start the App

The Flask development server runs on `127.0.0.1:5000` by default:

```powershell
python app.py
```

Default behavior:
- Binds to `http://127.0.0.1:5000/`
- Debug mode is enabled
- Auto-reload on code changes

To use Flask CLI with custom host/port:

```powershell
# Set FLASK_APP environment variable
$env:FLASK_APP = "app.py"
flask run --host=0.0.0.0 --port=8080
```

**Note:** Command-line arguments (`--host`, `--port`) are not accepted directly by `python app.py`. 
To modify the host/port, either:
1. Modify `app.py` to call `app.run(host='0.0.0.0', port=8080)`
2. Use Flask CLI: `flask run --host=0.0.0.0 --port=8080`
3. Use default settings: `python app.py` (runs on 127.0.0.1:5000)

Open in your browser:

- Root (auto-redirect): `http://127.0.0.1:5000/`
- Login page: `http://127.0.0.1:5000/login`
- Register page: `http://127.0.0.1:5000/register`

---

## 4. Configuration

All critical configuration lives in `app.py`.

### 4.1 Secret Key

Used for sessions and CSRF protection:

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'replace-with-a-strong-secret-key')
```

- The effective configuration key is `SECRET_KEY`.
- The environment variable name `FLASK_SECRET` is used when present to configure CSRF and session security.
- In production, you should use a strong, random secret and avoid hardcoding it in the source (for example, load from an environment variable and assign to `SECRET_KEY`).

### 4.2 Database

The project uses a SQLite database configured in `app.py`:

```python
app.config['DATABASE'] = 'app.db'
```

- Database file name: `app.db`
- Location: Root of the project directory
- The database is created automatically when the app starts
- `init_db(app)` creates the database and tables on startup if they do not exist
- Tables: `users` (id, username, password_hash, email)

**Note:** The previous documentation mentioning `data/database.sqlite3` is incorrect. The actual implementation uses `app.db` in the project root.

### 4.3 Sessions & Login

- Uses `Flask-Login` to manage user login state
- Sessions are stored server-side using Flask's default cookie-based session management
- Login view name: `auth.login`, mapped to `/login`
- Login manager is configured in app.py and enforces authentication for protected routes

---

## 5. Routes & Behavior

### 5.1 Blueprints and Entry Routes

`app.py` registers the auth blueprint and defines core routes:

- `/` (root):
  - If the user is authenticated: redirect to `/dashboard`
  - If not: redirect to `/login`
- `/dashboard`: login-protected homepage

`auth.py` (via `auth_bp`) provides authentication-related routes:

- `/register`: registration page (GET / POST)
- `/login`: login page (GET / POST)
- `/logout`: logout (GET)

**Note:** The route `/profile` mentioned in some documentation is NOT implemented. Only the routes listed above are available.

### 5.2 Route Summary

- `GET /` — root, redirects based on login state
- `GET /login` — display login form
- `POST /login` — process login
- `GET /register` — display registration form
- `POST /register` — process registration; typically redirects to `/dashboard` on success
- `GET /logout` — log out current user (requires authentication)
- `GET /dashboard` — authenticated dashboard view (protected by `@login_required`)

---

## 6. Forms and Validation Rules

The exact implementations live in `auth.py` and `models.py`. The following summarizes the expected behavior based on the current code.

### 6.1 Registration (`/register`)

Typical fields:

- `username`
  - Required
  - Minimum length: 3 characters
  - Maximum length: 32 characters
  - Must be unique in the database
- `email`
  - Required
  - Must be a valid email format
  - Must be unique in the database (prevents duplicate accounts)
- `password`
  - Required
  - Minimum length: **6 characters** (not 3 as previously documented)
  - Stored as a hash using Werkzeug password hashing

**Note:** Previous documentation stating minimum password length of 3 characters is incorrect. The actual minimum is 6.

### 6.2 Login (`/login`)

Fields:

- `username`
  - Required
  - Minimum length: 3 characters
  - Maximum length: 32 characters
- `password`
  - Required
  - Minimum length: 6 characters
  - Maximum length: 128 characters

Validation logic (conceptually):

- Look up the user by username
- Verify that the provided password matches the stored hash
- On success, log the user in via `Flask-Login` and redirect to `/dashboard`
- On failure, display "Invalid username or password" message

---

## 7. Data Model & Persistence

`models.py` is responsible for:

- Creating connections to the SQLite database (using `app.config['DATABASE']`)
- Defining the `User` model with fields: `id`, `username`, `email`, `password_hash`
- Providing user operations such as:
  - `User.create(...)`
  - `User.get_by_id(...)`
  - `User.get_by_username(...)`

`app.py` wires up `Flask-Login` with a `user_loader` that uses `User.get_by_id` to load the currently logged-in user:

```python
@login_manager.user_loader
def load_user(user_id):
    conn = get_connection(app)
    user = User.get_by_id(conn, int(user_id))
    conn.close()
    return user
```

---

## 8. Running Tests

The project includes comprehensive test coverage using pytest.

### 8.1 Using setup and test scripts (Recommended)

**Windows PowerShell:**
```powershell
# Setup environment (one-time)
.\setup.ps1

# Run tests
.\run_tests.ps1
```

**Bash/Linux:**
```bash
# Setup environment (one-time)
chmod +x setup.sh
./setup.sh

# Run tests
chmod +x run_tests.sh
./run_tests.sh
```

### 8.2 Manual test execution

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run all tests with verbose output
pytest test_app.py -v

# Run specific test class
pytest test_app.py::TestLogin -v

# Run with coverage report
pytest test_app.py --cov=.
```

### 8.3 Test Coverage

The test suite (`test_app.py`) includes:

- **TestAppStartup**: Verifies app configuration and blueprint registration
- **TestRoutes**: Tests all route accessibility and redirects
- **TestRegistration**: Tests user registration with validation
- **TestLogin**: Tests login flow and authentication
- **TestLogout**: Tests logout functionality
- **TestDatabase**: Tests database operations (user creation, lookup)
- **TestFormValidation**: Tests form structure and validators

Expected result: **All tests should pass**

---

## 9. Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Ensure virtual environment is activated and dependencies are installed:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: "sqlite3.IntegrityError: UNIQUE constraint failed"
**Solution:** Delete `app.db` and restart the app:
```powershell
Remove-Item app.db
python app.py
```

### Issue: "RuntimeError: Working outside of application context"
**Solution:** This occurs in test code outside Flask app context. Use `with app.app_context():` to wrap code.

### Issue: Port 5000 already in use
**Solution:** Use Flask CLI to specify different port:
```powershell
$env:FLASK_APP = "app.py"
flask run --port=5001
```

---

## 10. Quick Start Summary

```powershell
# 1. Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the app
python app.py

# 4. Open browser
# http://127.0.0.1:5000/

# 5. Run tests (optional)
pytest test_app.py -v
```

---

## Changes Made (From Original README)

This corrected version addresses the following issues:

1. ✅ Fixed command-line argument documentation (--host, --port don't work with `python app.py`)
2. ✅ Corrected database configuration from `data/database.sqlite3` to `app.db`
3. ✅ Updated password minimum length from 3 to 6 characters
4. ✅ Removed non-existent `/profile` route from documentation
5. ✅ Fixed incomplete code example in 3.2 section
6. ✅ Added testing documentation with pytest
7. ✅ Added troubleshooting section
8. ✅ Added quick start summary
9. ✅ Clarified session management (no Redis, using Flask default)
10. ✅ Fixed virtual environment activation path escaping

