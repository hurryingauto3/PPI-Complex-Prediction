from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_navigation import Navigation
from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()

@nav.navigation()
def mynavbar():
    return Navbar(
        '',
        View('Home', 'index'),
        View('Protien Networks', 'protnetwork'),
        # View('Clustering', 'clustering'),
        View('Statistics', 'statistics'))
# ...

app = Flask(__name__)
nav.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/protnetwork    ')
def protnetwork():
    return render_template('protnetwork.html')

@app.route('/clustering')
def clustervis():
    return render_template('clustering.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)