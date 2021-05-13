from flask import Flask, render_template, redirect, request, session
import sqlite3
import random
import string

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'K>~EEAnH_x,Z{q.43;NmyQiNz1^Yr7'

def reset_board():
    sql_query = f"UPDATE cells SET ship_id = NULL, empty = True"
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

def place_ship(ship_id, ship_length):
    valid_placement = False
    while not valid_placement:
        orientation = random.randint(0, 1)
        if orientation: # Horizontal orientation
            row = random.choice(string.ascii_uppercase[0:10])
            start_column = random.randint(1, 11-ship_length)
            cells = []
            for index in range(ship_length):
                column = start_column + index
                cells.append(row + str(column))
        else:
            column = random.randint(1, 10)
            start_row = random.randint(0, 10-ship_length)
            cells = []
            for index in range(ship_length):
                row = string.ascii_uppercase[start_row + index]
                cells.append(row + str(column))
        valid_placement = record_postion(cells, ship_id)
    return cells.copy()

def record_postion(coords, ship):
    for cell in coords:
        sql_query = f"SELECT ship_id FROM cells WHERE coordinates = '{cell}' AND empty = False"
        check_coord = execute_query(sql_query)
        if check_coord:
            return False
    for cell in coords:
        sql_query = f"UPDATE cells SET ship_id = {ship}, empty = False WHERE coordinates = '{cell}'"
        execute_query(sql_query)
    return True

def check_guess(guess):
    sql_query = f"SELECT ship_id FROM cells WHERE coordinates = '{guess}' AND empty = False"
    is_hit = execute_query(sql_query)
    if is_hit:
        sql_query = f"UPDATE cells SET guessed = 'Hit' WHERE coordinates = '{guess}'"
        session['hits'].append(guess)
    else:
        sql_query = f"UPDATE cells SET guessed = 'Miss' WHERE coordinates = '{guess}'"
        session['misses'].append(guess)
    session.modified = True
    execute_query(sql_query)

def player_ship(ship_name, orientation, start_cell):
    start_row = start_cell[0]
    start_column = int(start_cell[1:])
    cells = []
    fleet = ['Destroyer', 'Submarine', 'Crusier', 'Battleship', 'Carrier']
    if ship_name == 'Destroyer':
        ship_length = 2
    elif ship_name == 'Submarine' or ship_name == 'Crusier':
        ship_length = 3
    elif ship_name == 'Battleship':
        ship_length = 4
    else:
        ship_length = 5
    if orientation: # Horizontal orientation
        if start_column + ship_length - 1 > 10:
            return False
        for index in range(ship_length):
            column = start_column + index
            location = start_row + str(column)
            if location not in session['p_ships']:
                cells.append(location)
            else:
                return False
    else:
        col_index = string.ascii_uppercase.find(start_row)
        if col_index + ship_length -1 > string.ascii_uppercase.find('J'):
            return False
        for index in range(ship_length):
            start = string.ascii_uppercase.find(start_row)
            row = string.ascii_uppercase[start + index]
            location = row + str(start_column)
            if location not in session['p_ships']:
                cells.append(location)
            else:
                return False
        # valid_placement = record_postion(cells, fleet.index(ship_name)+1)
    session['p_fleet'].append(ship_name)
    session.modified = True
    return cells.copy()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        guess = request.form['guess']
        check_guess(guess)
    else:
        reset_board()
        place_ship(1, 2)
        place_ship(2, 3)
        place_ship(3, 3)
        place_ship(4, 4)
        place_ship(5, 5)
        session['hits'] = []
        session['misses'] = []
    columns = make_columns()
    rows = make_rows()
    return render_template("index.html", columns = columns, rows = rows)

@app.route('/player_board', methods=['GET', 'POST'])
def player_board():
    if request.method == 'POST':
        new_ship = request.form['new_ship']
        orientation = int(request.form['orientation'])
        start_cell = request.form['start_cell'].upper()
        result = player_ship(new_ship, orientation, start_cell)
        if result: 
            for cell in result:
                session['p_ships'].append(cell)
            session.modified = True
            feedback = 'Ship placed!'
        else:
           feedback = "Invalid placement!"
        print(session['p_fleet'])
    else:
        session['p_ships'] = []
        session['p_fleet'] = []
        feedback = ''
    ships = ['Destroyer','Submarine', 'Crusier','Battleship', 'Carrier']
    columns = make_columns()
    rows = make_rows()
    return render_template("player_board.html", columns = columns, rows = rows, ships=ships,
        feedback = feedback)

if __name__ == '__main__':
    app.run()