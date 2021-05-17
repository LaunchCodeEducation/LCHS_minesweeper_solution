import sqlite3

db = sqlite3.connect('game.db')
cursor = db.cursor()

cursor.execute("DROP TABLE IF EXISTS mines")
cursor.execute("DROP TABLE IF EXISTS map")

sql_query = """
    CREATE TABLE IF NOT EXISTS mines 
    (mine_id INTEGER PRIMARY KEY, coordinates TEXT NOT NULL)
    """
cursor.execute(sql_query)

sql_query = """
    CREATE TABLE IF NOT EXISTS map 
    (cell_id INTEGER PRIMARY KEY, coordinates TEXT NOT NULL, surr_mines INT, guessed TEXT,
    mine_id INT)
    """
cursor.execute(sql_query)

# The game is played on a 10x10 grid, but part of the logic requires the program
# to check the squares surrounding a cell. Rather than code different logic for
# edge and corner cells, adding an empty layer around the grid helps!

# Rows X and Y, and columns 0 and 11 remain empty and unseen to the players.
map_rows = 'XABCDEFGHIJY'
map_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
for row in map_rows:
    for column in map_columns:
        location = row + str(column)  # Produces a string like 'B4' for each cell.
        sql_query = f"INSERT INTO map (coordinates, guessed) VALUES ('{location}', False)"
        cursor.execute(sql_query)

db.commit()
db.close()