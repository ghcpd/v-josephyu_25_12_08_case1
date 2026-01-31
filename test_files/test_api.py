# Example script demonstrating programmatic register/login (handles CSRF tokens)
# This file is *not* a test. It is an example script.

try:
    import requests
    from bs4 import BeautifulSoup
except Exception:  # pragma: no cover - optional deps
    # If requests/bs4 aren't installed, avoid import errors during pytest collection.
    __test__ = False
else:
    BASE = 'http://127.0.0.1:5000'

    s = requests.Session()
    # GET register page
    r = s.get(BASE + '/register')
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input', {'name': 'csrf_token'})['value']

    # Register
    payload = {
        'username': 'apiuser',
        'email': 'api@example.com',
        'password': 'apipass',
        'csrf_token': csrf
    }
    resp = s.post(BASE + '/register', data=payload)
    print('Register status:', resp.status_code)

    # Access dashboard
    resp2 = s.get(BASE + '/dashboard')
    print('Dashboard status:', resp2.status_code)
    print(resp2.text[:200])
