from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_navigation import Navigation
from flask_nav import Nav
from flask_nav.elements import Navbar, View


app = Flask(__name__)
nav = Navigation(app)

nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('Protien Networks', 'protnetwork'),
    nav.Item('Clustering', 'clustervis'),
    nav.Item('Statistics', 'statistics')
])

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)