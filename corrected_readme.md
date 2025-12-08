# Flask User Login & Registration App (Corrected)

This project is a simple Flask-based user registration and login example. This corrected README fixes inaccuracies and provides working commands.

Requirements
- Python 3.10+
- pip
- (Recommended) virtual environment

Quick setup (PowerShell)

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

Start the app (PowerShell)

```powershell
# The project runs on 127.0.0.1:5000 by default when using `python app.py`.
python app.py

# To bind to a custom host/port using Flask CLI (recommended):
# 1. Set environment variables (PowerShell):
 #  $env:FLASK_RUN_HOST = '0.0.0.0'
 #  $env:FLASK_RUN_PORT = '8080'
# 2. Run:
#  flask run
```

Important fixes and notes
- Database file: the app uses `app.config['DATABASE'] = 'app.db'` (root). The README now reflects this.
- Email is required by the current `RegisterForm`. Update form or documentation depending on desired behavior.
- Password minimum length enforced by the code is 6 characters (WTForms validator). Updated docs accordingly.
- SESSIONLESS_MODE and Redis session storage are not implemented — those sections removed.

Routes
- `/` — redirects to login or dashboard
- `/login` — login form
- `/register` — register form (email required)
- `/logout` — logout
- `/dashboard` — protected route

Testing
Run tests with `pytest` after activating the virtual environment.
