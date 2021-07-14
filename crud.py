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

def record_mines(locations):
    pass

def count_mines():
    pass

def check_surroundings(location):
    count = 0
    rows = 'XABCDEFGHIJY'
    row = rows.find(location[0])
    column = int(location[1:])
    if 0 < row < 11 and 0 < column < 11:
        for current_row in rows[row-1:row+2]:
            for col_change in [-1, 0, 1]:
                current_column = column + col_change
                neighbor = current_row + str(current_column)
                sql_query = f"SELECT mine_id FROM mines WHERE coordinates = '{neighbor}'"
                mined = execute_query(sql_query)
                if mined and neighbor != location:
                    count += 1
        session['mine_counts'][location] = count
        session.modified = True
        sql_query = f"UPDATE board SET surr_mines = {count} WHERE coordinates = '{location}'"
        execute_query(sql_query)
