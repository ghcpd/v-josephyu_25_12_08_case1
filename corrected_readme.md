# Flask User Login & Registration App — Corrected README

This lightweight Flask example provides user registration and login pages, an authenticated dashboard, and a local SQLite datastore. The contents below reflect the current implementation in `app.py`, `auth.py`, and `models.py` and include working commands to run and test the app.

---

## 1. Requirements

- Python 3.10+ (the repo was tested on Python 3.13)
- `pip` available
- Recommended: a virtual environment to isolate dependencies

This project includes pytest tests and uses Flask, Flask-Login, and Flask-WTF.

---

## 2. Project Structure

```
.
├─ app.py               # App entrypoint, blueprints, login config
├─ auth.py              # Auth blueprint: register, login, logout
├─ models.py            # SQLite models & helpers
├─ templates/           # Jinja2 templates
├─ requirements.txt     # Pinned Python dependencies
├─ test_files/          # Unit tests used for verification
└─ README.md            # Original documentation (see corrected_readme.md for accurate guidance)
```

---

## 3. Installation & Running (Working Commands)

Below are cross-platform instructions for creating a virtual environment, installing dependencies, and running tests. These commands were verified as written in this project.

### 3.1 Create and activate a virtual environment

- Windows PowerShell (recommended):

```powershell
python -m venv .venv
# Activate the venv (PowerShell)
. .\.venv\Scripts\Activate.ps1
```

- UNIX / macOS / Git Bash / WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3.2 Install dependencies

Preferred (install pinned dependencies):

```powershell
pip install -r requirements.txt
```

Or, for quick manual installs (not recommended for reproducible runs):

```powershell
pip install flask flask-login flask-wtf wtforms
```

### 3.3 Start the App

This project uses `app.py` as a small runner that calls `app.run(debug=True)` by default. That means:

- Default listening address: http://127.0.0.1:5000
- If you run `python app.py --host=0.0.0.0 --port=8080` the flags will not be respected — the script doesn't parse CLI flags for host/port.

To run the app (default):

```powershell
python app.py
```

To change the bind address or port, edit `app.py` and pass the host/port to `app.run()` (example):

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

Open the following in your browser (default):

- Root: http://127.0.0.1:5000/
- Login: http://127.0.0.1:5000/login
- Register: http://127.0.0.1:5000/register

---

## 4. Configuration (Important)

- SECRET_KEY: Stored in `app.py` by default. For production, set a secure random secret and load from env vars.

Example inside `app.py`:

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'replace-with-a-strong-secret-key')
```

- DATABASE: default is `app.db` (project root). If you prefer a different path, set

```python
app.config['DATABASE'] = 'data/database.sqlite3'
```

and ensure the `data/` directory exists.

---

## 5. Sessions & Login

This demo uses Flask's default session mechanism together with Flask-Login. There is no Redis-backed session store implemented in `app.py` in this repository.

---

## 6. Routes & Behavior (Actual)

Implemented routes (auth blueprint + app):

- GET / — redirects to /dashboard if authenticated, otherwise /login
- GET /dashboard — requires login
- GET /login — login page
- POST /login — process login
- GET /register — register page
- POST /register — process registration
- GET /logout — log out current user

Note: `/profile` is not implemented in this codebase.

---

## 7. Forms & Validation (Actual)

- Registration requires: username, email and password.
  - `username` — required, 3..32 chars
  - `email` — required and must be unique (email is NOT optional in current code)
  - `password` — required, minimum length 6 (not 3)

---

## 8. Data model

- `app.config['DATABASE']` is the SQLite filename used by `models.get_connection()`.
- The `users` table includes:
  - id, username (UNIQUE NOT NULL), password_hash, email (UNIQUE NOT NULL)

---

## 9. Tests

This repo includes a small pytest suite under `test_files/`. To run the tests from the project root (with the venv active):

```bash
python -m pytest -q test_files
```

All tests (added/verified in the packaging step) assert the main functionality: registration, login, model persistence, and duplicate username behavior.

---

## 10. Notes & Known differences vs old docs

- This corrected file documents the actual code behavior. The original `README.md` included several incorrect statements such as: claims of Redis-backed sessions and sessionless mode, an optional email field, CLI-driven host/port overrides for `python app.py`, and a `/profile` route — none of which are implemented in this codebase.

If you'd like, I can either update `app.py` to support CLI-specified host/port and add optional profile/sessionless features, or I can keep the code minimal and maintain this corrected doc.
