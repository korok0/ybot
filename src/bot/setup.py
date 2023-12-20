import sqlite3

f = open("src/bot/members.db", "w")
f.close()

conn = sqlite3.connect("src/bot/members.db")

c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY,
          token TEXT
)""")
conn.commit()
conn.close()