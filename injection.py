import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT)")
cur.executemany("INSERT INTO users (username, email) VALUES (?, ?)", [
    ("alice", "alice@example.com"),
    ("bob", "bob@example.com"),
    ("admin", "admin@secret.local")
])
conn.commit()

print("DB ready: alice, bob, admin")
print("Try typing: alice  then  ' OR '1'='1")
print("-"*60)

def vulnerable_query(user_input):
    query = f"SELECT * FROM users WHERE username = '{user_input}'"
    print(f"\n[VULNERABLE] SQL -> {query}")
    cur.execute(query)
    print(f"Result: {cur.fetchall()}")

def safe_query(user_input):
    query = "SELECT * FROM users WHERE username = ?"
    print(f"\n[SAFE] SQL -> {query} | param={user_input!r}")
    cur.execute(query, (user_input,))
    print(f"Result: {cur.fetchall()}")

while True:
    user_input = input("\nEnter username (or 'exit'): ")
    if user_input.lower() == "exit":
        break
    vulnerable_query(user_input)
    safe_query(user_input)
