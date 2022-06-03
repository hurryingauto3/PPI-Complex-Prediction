from frontend import init_app
from algorithms.master import Master, Cluster, Database, Data
# from algorithms.clique_perc import Clique_Percolation, find_intensity
# from algorithms.evolalgo import Chromosome, evolAlgo
# from algorithms.cluster import Cluster

master = Master()
flaskapp = init_app(master)

if __name__ == '__main__':
    flaskapp.run(debug=True)