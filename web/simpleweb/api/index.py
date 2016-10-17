from .. import app
from .. import db
from ..models import Item
from flask import render_template, jsonify, request
from subprocess import Popen


@app.route('/')
def get():
    model = {'terms': [term[0] for term in db.session.execute('SELECT DISTINCT SEARCH FROM ITEMS').fetchall()]}
    return render_template('index.html', model=model)


@app.route('/data/')
def get_data():
    bins = request.args.get('bins')
    hist_sql = """
                SELECT R.SEARCH, R.BIN_N, R.BIN_B, R.BIN_E, COUNT(1)
                FROM (SELECT SEARCH,
                             ROUND((PRICE - M.MIN_PRICE) / ((M.MAX_PRICE - MIN_PRICE)/ {0}),0) AS BIN_N,
                             ROUND((PRICE - M.MIN_PRICE) / ((M.MAX_PRICE - MIN_PRICE)/ {0}),0)*ROUND(M.MAX_PRICE - MIN_PRICE,0) as BIN_B,
                             ROUND(((PRICE - M.MIN_PRICE) / ((M.MAX_PRICE - MIN_PRICE)/ {0}))+1,0)*ROUND(M.MAX_PRICE - MIN_PRICE,0) as BIN_E
                      FROM ITEMS
                      JOIN (SELECT MIN(PRICE) AS MIN_PRICE, MAX(PRICE) AS MAX_PRICE FROM ITEMS) AS M) AS R
                GROUP BY R.SEARCH, R.BIN_N, R.BIN_B, R.BIN_E
                ORDER BY R.SEARCH, R.BIN_N
                """.format(bins)

    items = []
    for single_item in Item.query.all():
        series = {}
        for s in items:
            if s['key'] == single_item.search.capitalize():
                series = s
                break
        if series == {}:
            series = {'key': single_item.search.capitalize(), 'values': []}
            items.append(series)

        series['values'].append({'x': len(series['values']), 'y': single_item.price})

    hist = []
    for term in db.session.execute(hist_sql).fetchall():
        series = {}
        for s in hist:
            if s['key'] == term[0].capitalize():
                series = s
                break
        if series == {}:
            series = {'key': term[0].capitalize(), 'values': []}
            hist.append(series)

        series['values'].append({'x': term[1], 'label': str(term[2]) + " - " + str(term[3]), 'y': term[4]})

    return jsonify({'data': items, 'histogram': hist})


@app.route('/crawl')
def crawl():
    search_term = request.args.get('search')
    process = Popen(['cmd.bat', search_term])
    return jsonify({'search_term': process.returncode})
