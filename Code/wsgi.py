from frontend import init_app
from algorithms.master import Master, Cluster, Database, Data

master = Master()
flaskapp = init_app(master)

if __name__ == '__main__':
    flaskapp.run(debug=True)