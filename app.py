from flask import Flask, render_template, redirect, url_for
import subprocess, sys, os

app = Flask(__name__)

GAMES = [
    {'slug': 'chess', 'name': 'Chess'},
    {'slug': 'rotating_box', 'name': 'Rotating Box'},
    {'slug': 'pong', 'name': 'Pong'},
]
EMPTY_SLOTS = 12 - len(GAMES)


@app.route('/')
def index():
    slots = GAMES + [{'slug': None, 'name': None}] * EMPTY_SLOTS
    return render_template('index.html', slots=slots)


@app.route('/game/<slug>')
def game(slug):
    game = next((g for g in GAMES if g['slug'] == slug), None)
    if not game:
        return redirect(url_for('index'))
    return render_template('game.html', game=game)


@app.route('/launch/<slug>')
def launch(slug):
    game = next((g for g in GAMES if g['slug'] == slug), None)
    if not game:
        return redirect(url_for('index'))
    if slug == 'chess':
        cmd = [sys.executable, '-m', 'chess.main']
    elif slug == 'rotating_box':
        path = os.path.join(os.getcwd(), 'rotating_box', 'rotating_box_simulation.py')
        cmd = [sys.executable, path]
    elif slug == 'pong':
        path = os.path.join(os.getcwd(), 'pong', 'pong.py')
        cmd = [sys.executable, path]
    else:
        return redirect(url_for('game', slug=slug))
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return redirect(url_for('game', slug=slug))


if __name__ == '__main__':
    app.run(debug=True)
