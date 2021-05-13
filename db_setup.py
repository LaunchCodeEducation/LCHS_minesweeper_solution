import sqlite3
import string

ships = [['Destroyer', 2], ['Submarnine', 3], ['Crusier', 3], ['Battleship', 4], ['Carrier', 5]]
rows = string.ascii_uppercase[0:10]
columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

db = sqlite3.connect('game.db')
cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS ships")
cursor.execute("DROP TABLE IF EXISTS cells")
cursor.execute("DROP TABLE IF EXISTS mines")
cursor.execute("DROP TABLE IF EXISTS map")

sql_query = """
    CREATE TABLE IF NOT EXISTS ships 
    (ship_id INTEGER PRIMARY KEY, name TEXT NOT NULL, length INT NOT NULL)
    """
cursor.execute(sql_query)

sql_query = """
    CREATE TABLE IF NOT EXISTS cells 
    (cell_id INTEGER PRIMARY KEY, coordinates TEXT NOT NULL, ship_id INT, empty BOOLEAN, guessed TEXT,
    FOREIGN KEY (ship_id)
       REFERENCES ships (ship_id))
    """
cursor.execute(sql_query)

sql_query = """
    CREATE TABLE IF NOT EXISTS mines 
    (mine_id INTEGER PRIMARY KEY, coordinates TEXT NOT NULL, guessed TEXT)
    """
cursor.execute(sql_query)

sql_query = """
    CREATE TABLE IF NOT EXISTS map 
    (cell_id INTEGER PRIMARY KEY, coordinates TEXT NOT NULL, surr_mines INT, guessed TEXT,
    mine_id INT,
    FOREIGN KEY (mine_id)
       REFERENCES ships (mine_id))
    """
cursor.execute(sql_query)

for ship in ships:
    sql_query = f"INSERT INTO ships (name, length) VALUES ('{ship[0]}', {ship[1]})"
    cursor.execute(sql_query)

for row in rows:
    for column in columns:
        location = row + str(column)
        sql_query = f"INSERT INTO cells (coordinates, empty) VALUES ('{location}', True)"
        cursor.execute(sql_query)

map_rows = 'XABCDEFGHIJY'
map_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
for row in map_rows:
    for column in map_columns:
        location = row + str(column)
        sql_query = f"INSERT INTO map (coordinates, guessed) VALUES ('{location}', False)"
        cursor.execute(sql_query)

db.commit()
db.close()