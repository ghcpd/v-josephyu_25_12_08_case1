import sys
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app

with app.test_client() as c:
    rv = c.post('/register', data={'username': 'tester', 'password': 'safepass', 'email': 't@example.com'}, follow_redirects=True)
    print('Status:', rv.status_code)
    print(rv.request.path)
    print(rv.data.decode('utf-8'))
