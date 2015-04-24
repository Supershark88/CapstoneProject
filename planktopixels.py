from flask import Flask, render_template
from flask_wtf import Form
import sqlite3
from contextlib import closing

# configuration
DATABASE = './planktopixels.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

if __name__ == "__main__":
    from os import environ
    if 'WINGDB_ACTIVE' in environ:
        app.debug = False
    app.run(use_reloader=True)