from flask import session
import sqlite3

def execute_query(query_string):
    db = sqlite3.connect('game.db')
    cursor = db.cursor()
    if "select" in query_string.lower():
        try:
            results = list(cursor.execute(query_string))
        except:
            results = 'error'
    else:
        try:
            cursor.execute(query_string)
            db.commit()
            results = 'success'
        except:
            results = 'error'
    db.close()
    return results

def record_mines(coords):
    pass

def count_mines():
    pass

def check_surroundings(cell):
    count = 0
    rows = 'XABCDEFGHIJY'
    row = rows.find(cell[0])
    column = int(cell[1:])
    for check_row in rows[row-1:row+2]:
        for col_change in range(-1, 2):
            check_column = column + col_change
            location = check_row + str(check_column)
            sql_query = f"SELECT mine_id FROM mines WHERE coordinates = '{location}'"
            mined = execute_query(sql_query)
            if mined and location != cell:
                count += 1
    session['mine_counts'][cell] = count
    session.modified = True
    sql_query = f"UPDATE board SET surr_mines = {count} WHERE coordinates = '{cell}'"
    execute_query(sql_query)
