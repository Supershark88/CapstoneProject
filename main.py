from flask import Flask, render_template
from flask_wtf import Form

app = Flask(__name__)

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