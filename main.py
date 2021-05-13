from flask import Flask, render_template, redirect, request, session
import sqlite3
import random
import string

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'K>~EEAnH_x,Z{q.43;NmyQiNz1^Yr7'

def reset_board():
    sql_query = "UPDATE map SET mine_id = NULL, guessed = NULL"
    execute_query(sql_query)
    sql_query = "DELETE FROM mines WHERE mine_id >= 1"
    execute_query(sql_query)

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

def make_columns():
    numbers = ['']
    for index in range(10):
        numbers.append(index+1)
    return numbers.copy()

def make_rows():
    rows = []
    for index in range(10):
        row = []
        for entry in range(11):
            letter = string.ascii_uppercase[index]
            if entry == 0:
                row.append(letter)
            else:
                row.append(letter + str(entry))
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

def count_mines():
    sql_query = "SELECT coordinates FROM map"
    cells = execute_query(sql_query)
    for cell in cells:
        check_surroundings(cell[0])

def check_surroundings(cell):
    count = 0
    rows = 'XABCDEFGHIJY'
    row = rows.find(cell[0])
    column = int(cell[1:])
    for check_row in rows[row-1:row+2]:
        for col_change in range(-1, 2):
            check_column = column + col_change
            location = check_row + str(check_column)
            sql_query = f"SELECT * FROM mines WHERE coordinates = '{location}'"
            mined = execute_query(sql_query)
            if mined:
                count += 1
    session['mine_counts'][cell] = count
    session.modified = True
    sql_query = f"UPDATE map SET surr_mines = {count} WHERE coordinates = '{cell}'"
    execute_query(sql_query)

def record_mines(coords):
    counter = 1
    for cell in coords:
        sql_query = f"INSERT INTO mines (coordinates) VALUES ('{cell}')"
        execute_query(sql_query)
        sql_query = f"UPDATE map SET mine_id = {counter} WHERE coordinates = '{cell}'"
        execute_query(sql_query)
        counter += 1

def check_guess(guess, flag):
    safe_guess = True
    if flag:
        sql_query = f"UPDATE mines SET guessed = True WHERE coordinates = '{guess}'"
        execute_query(sql_query)
        session['flags'].append(guess)
        session['num_mines'] -= 1
    else:
        sql_query = f"SELECT * FROM map WHERE coordinates = '{guess}' AND mine_id IS NULL"
        result = execute_query(sql_query)
        if result:
            sql_query = f"UPDATE map SET guessed = True WHERE coordinates = '{guess}'"
            execute_query(sql_query)
            sql_query = f"SELECT surr_mines FROM map WHERE coordinates = '{guess}'"
            session['guesses'].append(guess)
        else:
            safe_guess = False        
    session.modified = True
    return safe_guess

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['num_mines'] = int(request.form['num_mines'])
        if session['num_mines'] == 0:
            session['num_mines'] = 10
        reset_board()
        session['mines'] = place_mines(session['num_mines'])
        return redirect('/play')
    else:
        reset_board()
        session['flags'] = []
        session['guesses'] = []
        session['mine_counts'] = {}
        session['hit_mine'] = False
    columns = make_columns()
    rows = make_rows()
    return render_template("index.html", columns = columns, rows = rows,
        page_title = "Play Minesweeper")

@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        guess = request.form['guess']
        if guess.lower() == 'restart':
            return redirect('/')
        flagged = request.form.get('flagged')
        safe_guess = check_guess(guess, flagged)
        if not safe_guess:
            session['hit_mine'] = True
    else:
        pass

    columns = make_columns()
    rows = make_rows()
    return render_template("mines.html", columns = columns, rows = rows,
        page_title = "Mines Remaining")

if __name__ == '__main__':
    app.run()