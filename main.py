from flask import Flask, render_template, redirect, request, session
import sqlite3
import random
import string

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'K>~EEAnH_x,Z{q.43;NmyQiNz1^Yr7'

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
                row.append([letter + str(entry), 'empty'])
        rows.append(row)
    return rows.copy()

def place_ships(ship_length = 5):
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
    return cells.copy()

@app.route('/', methods=['GET', 'POST'])
def index():
    columns = make_columns()
    rows = make_rows()
    session['cells'] = place_ships()
    return render_template("index.html", columns = columns, rows = rows)

if __name__ == '__main__':
    app.run()