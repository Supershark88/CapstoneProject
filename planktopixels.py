# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import pprint

# configuration
DATABASE = './planktopixels.db'
DEBUG = True
SECRET_KEY = 'Noah Zingler development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('PLANKTOPIXELS_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select id, date, username, temp, turbidity, ' \
                       'salinity, do, fish, crabs, shrimp, phytoA, phytoB, ' \
                       'phytoC, phytoD, phytoE, phytoF, phytoG, phytoH, phytoI, ' \
                       'zooJ, zooK, zooL, notes from entries order by id asc')
    entries = [dict(id=row[0], date=row[1], username=row[2], 
                    temp=row[3], turbidity=row[4], salinity=row[5], do=row[6], 
                    fish=row[7], crabs=row[8], shrimp=row[9], phytoA=row[10], 
                    phytoB=row[11], phytoC=row[12], phytoD=row[13], 
                    phytoE=row[14], phytoF=row[15], phytoG=row[16], 
                    phytoH=row[17], phytoI=row[18], zooJ=row[19], zooK=row[20], 
                    zooL=row[21], notes=row[22]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    #print ("got here", request.form['date'], #request.form['username'], request.form['temp'], 
                  #request.form['turbidity'], request.form['salinity'], 
                  #request.form['do'], request.form['fish'], request.form['crabs'], 
                  #request.form['shrimp'], request.form['phytoA'], 
                  #request.form['phytoB'], request.form['phytoC'], 
                  #request.form['phytoD'], request.form['phytoE'], 
                  #request.form['phytoF'], request.form['phytoG'], 
                  #request.form['phytoH'], request.form['phytoI'], 
                  #request.form['zooJ'], request.form['zooK'], 
                  #request.form['zooL'], 
                  #request.form['notes'])
    g.db.execute('insert into entries (date, username, temp, turbidity, salinity, do, '
                 'fish, crabs, shrimp, phytoA, phytoB, phytoC, phytoD, phytoE, phytoF, '
                 'phytoG, phytoH, phytoI, zooJ, zooK, zooL, notes) values (?, ?, ?, '
                 '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 [request.form['date'], request.form['username'], request.form['temp'], 
                  request.form['turbidity'], request.form['salinity'], 
                  request.form['do'], request.form['fish'], request.form['crabs'], 
                  request.form['shrimp'], request.form['phytoA'], 
                  request.form['phytoB'], request.form['phytoC'], 
                  request.form['phytoD'], request.form['phytoE'], 
                  request.form['phytoF'], request.form['phytoG'], 
                  request.form['phytoH'], request.form['phytoI'], 
                  request.form['zooJ'], request.form['zooK'], 
                  request.form['zooL'], request.form['notes']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))



if __name__ == "__main__":
    from os import environ
    if 'WINGDB_ACTIVE' in environ:
        app.debug = True
    app.run(use_reloader=True)