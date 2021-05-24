from flask import Flask, render_template, redirect, request, session
from game_logic import *
import string

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'K>~EEAnH_x,Z{q.43;NmyQiNz1^Yr7'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        num_mines = request.form['num_mines']
        if num_mines == '' or not num_mines.isdigit():
            session['num_mines'] = 10
        else:
            session['num_mines'] = int(num_mines)
        session['mines'] = place_mines(session['num_mines'])
        return redirect('/play')
    else:    
        reset_board()
    return render_template("index.html", page_title = "Play Minesweeper")

@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        guess = request.form['guess']
        if guess == '' or guess[0] not in string.ascii_uppercase[0:10]:
            return redirect('/')  
        flagged = request.form.get('flagged')
        safe_guess = check_guess(guess, flagged)
        if not safe_guess:
            session['hit_mine'] = True
    else:
        if session['num_mines'] <= 0:
            return redirect('/')
    page_title = f"Mines Remaining: {session['num_mines']}"
    return render_template("mines.html", page_title = page_title)

if __name__ == '__main__':
    app.run()
