from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/database')
def database():
    items = [
        {'id': 1, 'name': 'TP53', 'barcode': '893212299897', 'price': 500},
        {'id': 2, 'name': 'TNF', 'barcode': '123985473165', 'price': 900},
        {'id': 3, 'name': 'EGFR', 'barcode': '231985128446', 'price': 150}
    ]
    return render_template('database.html', items=items)

@app.route('/research')
def research():
    return render_template('research.html')

from pymongo import MongoClient
from bson.json_util import dumps, loads
from DatabaseOG import Database

@app.route('/test')
def test():
    db = Database()
    prot = dumps(db.get_all_prots(), indent=1)
    return prot