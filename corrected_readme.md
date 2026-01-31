# Flask User Login & Registration App (Corrected)

This project is a simple Flask-based user registration and login example.

Main fixes applied relative to original README:
- The app now uses data/database.sqlite3 by default (and will create the data/ directory if missing).
- The `app.py` entrypoint accepts `--host` and `--port` command-line flags to control the bind address and port.
- Registration requires an email and enforces password minimum length 6 (corrected documentation to match code).
- Forms use CSRF protection (Flask-WTF). Programmatic POSTs must fetch the CSRF token from the form and include it in the POST data.
- The documentation no longer claims Redis-backed sessions or SESSIONLESS_MODE (these were not implemented).
- Fixed broken fences and typos in the original README and added test instructions.

---

## Requirements

- Python 3.10+
- pip
- Recommended: a virtual environment to isolate dependencies

## Installation & Run (Windows PowerShell / Bash)

# Create and activate virtual environment (Windows PowerShell)
# Create virtual environment
python -m venv .venv
# Activate virtual environment
. \.venv\Scripts\Activate.ps1

# Bash (Linux/macOS)
python -m venv .venv
source .venv/bin/activate

### Install Dependencies

Install pinned requirements:

pip install -r requirements.txt

Or for quick testing:

pip install flask flask-login flask-wtf wtforms email_validator pytest

### Start the App

You can pass host and port via command line flags (the app will accept these flags):

python app.py --host=0.0.0.0 --port=8080

Default bind is 127.0.0.1:5000 when no flags are provided.

Open in your browser:

- Root (auto-redirect): http://127.0.0.1:5000/
- Login page: http://127.0.0.1:5000/login
- Register page: http://127.0.0.1:5000/register

### Database

- Default DB file: `data/database.sqlite3` (created automatically on startup)

### Forms & CSRF

- The forms use Flask-WTF CSRF protection. If you need to programmatically POST, fetch the page first to extract `csrf_token` and include it in POST payloads.

---

## Routes & Behavior (summary)

- GET / — redirect based on login state
- GET /login — display login form
- POST /login — process login (requires CSRF token for programmatic posts)
- GET /register — display registration form
- POST /register — process registration (requires CSRF token for programmatic posts)
- GET /logout — log out current user
- GET /dashboard — authenticated dashboard view (protected by @login_required)

---

## Tests

Run the automated tests (pytest):

pytest -q

# Notes for test automation
- Tests use Flask's test_client and rely on the local SQLite DB created under `data/`.
- For programmatic form submissions, the tests demonstrate fetching CSRF tokens from GET responses and adding them to subsequent POSTs.

---

If you want to run the example flow manually, the test_files/ directory includes example scripts showing how to perform the register/login flow programmatically (they demonstrate CSRF handling).
