from flask import Flask
from flask_bootstrap import Bootstrap
from flask_navigation import Navigation
from flask_nav import Nav
from flask_nav.elements import Navbar, View

def init_app(PPIDb, Cluster):
    app = Flask(__name__)
    app.config['DEBUG'] = True
    nav = Navigation(app)
    
    with app.app_context():
        #create Nav Bar
        nav.Bar('top', [
            nav.Item('Home', 'index'),
            nav.Item('Protien Networks', 'protnetwork'),
            nav.Item('Clustering', 'clustervis'),
            nav.Item('Statistics', 'statistics')
        ])
        nav.init_app(app)
        # Import parts of our core Flask app
        from . import routes
        # Import Dash application for protein networks
        from .dash_app1.dashboard import create_dashboard
        app = create_dashboard(app, PPIDb, Cluster)
        
        return app