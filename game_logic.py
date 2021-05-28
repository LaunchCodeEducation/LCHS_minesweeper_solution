import random
import string
from crud import *

def reset_board():
    sql_query = "UPDATE board SET mine_id = NULL, guessed = False, surr_mines = NULL"
    execute_query(sql_query)
    sql_query = "DELETE FROM mines WHERE mine_id >= 1"
    execute_query(sql_query)
    session['num_mines'] = 0
    session['flags'] = []
    session['guesses'] = []
    session['mine_counts'] = {}
    session['hit_mine'] = False
    session['mines'] = []
    if 'columns' not in session:
        session['columns'] = make_columns()
        session['rows'] = make_rows()

def make_columns():
    headings = ['']
    for label in range(10):
        headings.append(label+1)
    return headings.copy()

def make_rows():
    rows = []
    for index in range(10):
        row = []
        for column in range(11):
            letter = string.ascii_uppercase[index]
            if column == 0:
                row.append(letter)
            else:
                row.append(letter + str(column))
        rows.append(row)
    return rows.copy()

def place_mines(amount):
    mines = []
    while len(mines) < amount:
        row = random.choice(string.ascii_uppercase[0:10])
        column = random.randint(1, 10)
        location = row + str(column)
        if location not in mines:
            mines.append(location)
    mines.sort()
    record_mines(mines)
    count_mines()
    return mines.copy()

def check_guess(guess, flag):
    safe_guess = True
    if flag:
        session['flags'].append(guess)
        session['num_mines'] -= 1
        if guess in session['mines']:
            session['mines'].remove(guess)
            session.modified = True
    else:
        sql_query = f"SELECT * FROM board WHERE coordinates = '{guess}' AND mine_id IS NULL"
        no_mine = execute_query(sql_query)
        if no_mine:
            if guess in session['flags']:
                session['flags'].remove(guess)
                session['num_mines'] += 1
            session['guesses'].append(guess)
        else:
            safe_guess = False        
    session.modified = True
    sql_query = f"UPDATE board SET guessed = True WHERE coordinates = '{guess}'"
    execute_query(sql_query)
    return safe_guess