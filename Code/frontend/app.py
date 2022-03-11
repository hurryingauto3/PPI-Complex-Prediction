from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_navigation import Navigation
from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()

@nav.navigation()
def mynavbar():
    return Navbar(
        'mysite',
        View('Home', 'index'),
        View('About', 'about'),
        View('Contact', 'contact'),
    )

# ...

app = Flask(__name__)
nav.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/networks')
def protnetwork():
    return render_template('protnetwork.html')

@app.route('/clustering')
def clustervis():
    return render_template('clustering.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

if __name__ == '__main__':
    app.run(debug=True)