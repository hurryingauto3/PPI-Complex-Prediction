from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_navigation import Navigation

app = Flask(__name__)
nav = Navigation(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/protnetwork')
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