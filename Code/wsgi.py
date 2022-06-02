from frontend import init_app
from algorithms.database.DatabaseOG import Database, Data
from algorithms.clique_perc import Clique_Percolation, find_intensity
from algorithms.evolalgo import Chromosome, evolAlgo
from algorithms.cluster import Cluster

PPIDb = Database()
Cluster = Cluster()
flaskapp = init_app(PPIDb, Cluster)

if __name__ == '__main__':
    flaskapp.run(debug=True)