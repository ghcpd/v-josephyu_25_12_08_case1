import sqlite3
DB='app.db'
conn=sqlite3.connect(DB)
cur=conn.cursor()
cur.execute("SELECT id, username, email FROM users")
rows=cur.fetchall()
print('Users:', rows)
conn.close()
