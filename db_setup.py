import sqlite3
import string

ships = ['Destroyer', 'Submarnine', 'Crusier', 'Battleship', 'Carrier']
rows = string.ascii_uppercase[0:10]
columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

db = sqlite3.connect('game.db')
cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS posts")

sql_query = """
    CREATE TABLE IF NOT EXISTS users 
    (user_id INTEGER PRIMARY KEY, username TEXT NOT NULL)
    """
cursor.execute(sql_query)

sql_query = """
    CREATE TABLE IF NOT EXISTS posts 
    (post_id INTEGER PRIMARY KEY, user_id INT NOT NULL, entry TEXT, time TEXT,
    FOREIGN KEY (user_id)
       REFERENCES users (user_id))
    """
cursor.execute(sql_query)

for user in users:
    sql_query = f"INSERT INTO users (username) VALUES ('{user}')"
    cursor.execute(sql_query)

for post in posts:
    rand_id = random.randint(1, len(users))
    sql_query = f"INSERT INTO posts (user_id, entry, time) VALUES ({rand_id}, '{post}', '{datetime.datetime.now()}')"
    cursor.execute(sql_query)

db.commit()
db.close()