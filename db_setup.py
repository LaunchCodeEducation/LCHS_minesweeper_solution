import sqlite3

# Initialise the database and cursor objects here:


# Write SQL queries to create the 'mines' and 'board' tables:


# The game is played on a 10x10 grid, but part of the logic requires the program
# to check the squares surrounding a cell. Rather than code different logic for
# edge and corner cells, adding an empty layer around the grid helps!

# Rows X and Y, and columns 0 and 11 remain empty and unseen to the players.
board_rows = 'XABCDEFGHIJY'
board_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# Use nested for loops to add rows to the 'board' table:
