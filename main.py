from flask import Flask, render_template, redirect, request, session
from game_logic import *

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'K>~EEAnH_x,Z{q.43;NmyQiNz1^Yr7'

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

    columns = make_columns()
    rows = make_rows()
    page_title = f"Mines Remaining: {session['num_mines']}"
    return render_template("mines.html", columns = columns, rows = rows,
        page_title = page_title)

if __name__ == '__main__':
    app.run()