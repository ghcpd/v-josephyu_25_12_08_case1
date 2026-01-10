# Flask User Login & Registration App (Corrected)

This document reflects the project's actual behavior and provides reproducible setup and run instructions.

Requirements
- Python 3.10+ (Windows PowerShell or Bash examples included)
- pip
- Recommended: use the provided scripts to create a virtual environment

Quick start (Windows PowerShell)

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -q

# Start the app (development)
python app.py
# The app binds to 127.0.0.1:5000 by default when invoked this way.
```

Quick start (Linux / macOS)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python app.py
```

Notes and corrections relative to the original README
- Database path: The code uses app.config['DATABASE'] = 'app.db' in app.py. The DB file is created at the repository root, not in a data/ subdirectory. You can override the path by setting app.config['DATABASE'] before calling init_db(app).
- Run flags: Running `python app.py --host=0.0.0.0 --port=8080` is not supported by the current app entrypoint; call `python -m flask run --host=0.0.0.0 --port=8080` with `FLASK_APP=app.py` instead, or modify app.py to accept CLI args.
- Forms: Registration requires an email (DataRequired) and passwords are enforced to be at least 6 characters by the current RegisterForm. Update your expectations accordingly.
- Missing features: There is no /profile route implemented. The README previously referenced a profile update route; that route is not present in auth.py.
- Session storage: The README suggested server-side session storage in Redis and a SESSIONLESS_MODE. Those features are not implemented in the current codebase.

Routes summary (accurate)
- GET / — Redirects to /dashboard (if logged in) or /login
- GET /login — Show login form
- POST /login — Process login
- GET /register — Show registration form
- POST /register — Process registration and log in
- GET /logout — Log out user
- GET /dashboard — Login-protected dashboard

Testing
- Run `pytest -q` to execute unit tests. Tests are included in the `tests/` directory and will create a temporary database for isolation.

If you want these README-documented features (profile route, Redis-backed sessions, custom CLI host/port flags), open an issue or submit a patch to implement them.
