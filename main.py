from flask import Flask, render_template, redirect, request, session
from game_logic import *

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'K>~EEAnH_x,Z{q.43;NmyQiNz1^Yr7'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_mines = request.form['num_mines']
        if not num_mines or num_mines.isalpha():
            session['num_mines'] = 10
        else:
            session['num_mines'] = int(num_mines)
        session['mines'] = place_mines(session['num_mines'])
        return redirect('/play')
    else:
        session['flags'] = []
        session['guesses'] = []
        session['mine_counts'] = {}
        session['hit_mine'] = False
    session['columns'] = make_columns()
    session['rows'] = make_rows()
    return render_template("index.html", page_title = "Play Minesweeper")

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

    page_title = f"Mines Remaining: {session['num_mines']}"
    return render_template("mines.html", page_title = page_title)

if __name__ == '__main__':
    app.run()