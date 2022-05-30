from flask import render_template
from flask import current_app as app

@app.route('/')
def index():
    iframe = '/dashapp/'
    return render_template('index.html', iframe = iframe)

@app.route('/protnetwork')
def protnetwork():
    return render_template('protnetwork.html')

@app.route('/clustering')
def clustervis():
    return render_template('clusters.html')

@app.route('/statistics')
def statistics():
    stats = [1, 2, 3, 4, 5]
    return render_template('statistics.html', stats=stats)