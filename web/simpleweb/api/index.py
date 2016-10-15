from .. import app
from flask import render_template, jsonify

@app.route('/')
def get():
    return render_template('index.html', name='Title')

@app.route('/data/')
def get_data():
    data = {
        'key': 1,
        'key2': 'teste'
    }
    return jsonify(**data)
