from flask import Flask, render_template, redirect, request, session
from game_logic import *
import string

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'K>~EEAnH_x,Z{q.43;NmyQiNz1^Yr7'

@app.route('/', methods=['GET', 'POST'])
def index():     
    reset_board()
    return render_template("index.html", page_title = "Play Minesweeper")

@app.route('/play', methods=['GET', 'POST'])
def play():
    return render_template("mines.html", page_title = "Mines Remaining: ???")

if __name__ == '__main__':
    app.run()
