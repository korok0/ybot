import sqlite3

conn = sqlite3.connect("C:\\Users\\Vinea\\Desktop\\Personal Projects\\ybot\\src\\bot\\members.db")
c = conn.cursor()

c.execute("SELECT * FROM users")

a = c.fetchall()
print(a)
print(type(a))


# 258375730583306241
c.execute(f"SELECT token FROM users WHERE id={258375730583306241}")
print(c.fetchall()[0][0])
conn.commit()
c.execute(f"SELECT id FROM users WHERE id<{258375730583306241}")
print(c.fetchall())
conn.close()