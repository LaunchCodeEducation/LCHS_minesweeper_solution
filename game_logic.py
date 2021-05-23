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
    numbers = ['']
    for index in range(10):
        numbers.append(index+1)
    return numbers.copy()

def make_rows():
    rows = []
    for index in range(10):
        row = []
        for number in range(11):
            letter = string.ascii_uppercase[index]
            if number == 0:
                row.append(letter)
            else:
                row.append(letter + str(number))
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
        sql_query = f"UPDATE mines SET guessed = True WHERE coordinates = '{guess}'"
        execute_query(sql_query)
        session['flags'].append(guess)
        session['num_mines'] -= 1
        if guess in session['mines']:
            session['mines'].remove(guess)
            session.modified = True
    else:
        sql_query = f"SELECT * FROM board WHERE coordinates = '{guess}' and mine_id IS NULL"
        no_mine = execute_query(sql_query)
        if no_mine:
            if guess in session['flags']:
                session['flags'].remove(guess)
                session['num_mines'] += 1
            sql_query = f"UPDATE board SET guessed = True WHERE coordinates = '{guess}'"
            execute_query(sql_query)
            session['guesses'].append(guess)
        else:
            safe_guess = False        
    session.modified = True
    return safe_guess