from .. import app
from ..models import Item
from flask import render_template, jsonify, request
from subprocess import Popen

@app.route('/')
def get():
    return render_template('index.html', name='Title')


@app.route('/data/')
def get_data():
    items = [{'x': i, 'y': single_item.price} for i, single_item in enumerate(Item.query.all())]
    return jsonify({'data': [{
            'values': items,
            'key': 'Sine Wave',
            'color': '#ff7f0e'
        }]})

@app.route('/crawl')
def crawl():
    search_term = request.args.get('search')
    process = Popen(['cmd.bat', search_term])
    return jsonify({'search_term': process.returncode})
