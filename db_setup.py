import sqlite3

db = sqlite3.connect('game.db')
cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS mines")
cursor.execute("DROP TABLE IF EXISTS board")

sql_query = """
    CREATE TABLE IF NOT EXISTS mines 
    (mine_id INTEGER PRIMARY KEY, coordinates TEXT NOT NULL)
"""

cursor.execute(sql_query)

sql_query = """
    CREATE TABLE IF NOT EXISTS board 
    (cell_id INTEGER PRIMARY KEY, coordinates TEXT NOT NULL,
    surr_mines INT, guessed BOOL, mine_id INT)
    """

cursor.execute(sql_query)

board_rows = 'XABCDEFGHIJY'
board_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

for row in board_rows:
    for column in board_columns:
        location = row + str(column)
        sql_query = f"INSERT INTO board (coordinates, guessed) VALUES ('{location}', False)"
        cursor.execute(sql_query)

db.commit()
db.close()