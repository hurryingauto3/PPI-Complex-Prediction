from flask import render_template
from flask import current_app as app

@app.route('/')
def index():
    # iframe = '/dashapp/'
    return render_template('index.html')

@app.route('/protnetwork')
def protnetwork():
    iframe = '/dashapp/'
    return render_template('protnetwork.html', iframe = iframe)

@app.route('/clustering')
def clustervis():
    iframe = '/dashapp2/'
    return render_template('clusters.html', iframe = iframe)

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')