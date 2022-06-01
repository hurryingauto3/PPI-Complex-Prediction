from frontend import init_app
from algorithms.database.DatabaseOG import Database, Data

PPIDb = Database()
flaskapp = init_app(PPIDb)

if __name__ == '__main__':
    flaskapp.run(debug=True)