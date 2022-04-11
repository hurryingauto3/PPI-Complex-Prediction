from knapsack import *
from graphcol import *
from tsp import *

key = {"fp": "Fitness Proportion", "bt": "Binary Tournament", "tr": "Truncation", "rd": "Random", "rb": "Rank Based"}
selectionschemes = [('fp', 'rd'), ('rb', 'tr'), ('tr', 'tr'), ('rd', 'rd'),('fp', 'tr'),('rb','fp'), ('rd', 'tr'), ('tr', 'rb'), ('rb', 'rd'), ('rd','fp')]

nPop = 30
nOffspring = 10
nGen = 100
rMutation = 0.4
nIter = 40

f = open("log.txt", "w")
f.write("Parent Selection,Survivor Selection,Best Fitness,Average Fitness")
log = []
for i in selectionschemes:
    ks = knapsack("f2_l-d_kp_20_878", nPop, nOffspring, nGen, rMutation, nIter, i[0], i[1], False)
    try:
        ks.run()
    except ValueError:
        continue
    filename = "report/images/knapsack_"+i[0]+"_"+i[1]+".png"
    best_fitness = max(ks.bestFitnesses)
    avg_fitness = np.mean(ks.avgFitnesses)
    log.append((key[i[0]], key[i[1]], round(best_fitness, 2), round(avg_fitness, 2)))
    ks.plot("Total Value", filename.split(".")[0])
    del ks
    print("Knapsack completed with " + i[0] + " and " + i[1] + " selection schemes")
f.write("Knapsack")
for i in log:
    f.write(str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + "," + str(i[3]) + "\n")
log = []
for i in selectionschemes:
    gc = graphcoloring("gc-ds.txt",nPop, nOffspring, nGen, rMutation, nIter, i[0], i[1], True)
    try:
        gc.run()
    except ValueError:
        continue
    filename = "report/images/graphcoloring_"+i[0]+"_"+i[1]+".png"
    best_fitness = min(gc.bestFitnesses)
    avg_fitness = np.mean(gc.avgFitnesses)
    log.append((key[i[0]], key[i[1]], round(best_fitness, 2), round(avg_fitness, 2)))
    gc.plot("Total Violations", filename.split(".")[0])
    del gc
    print("Graph Coloring completed with " + i[0] + " and " + i[1] + " selection schemes")
f.write("Graph Coloring")
for i in log:
    f.write(str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + "," + str(i[3]) + "\n")
log = []
for i in selectionschemes:
    tsp = TSP("tsp-ds.tsp", nPop, nOffspring, nGen, rMutation, nIter, i[0], i[1], True)
    try:
        tsp.run()
    except ValueError:
        continue
    filename = "report/images/tsp_"+i[0]+"_"+i[1]+".png"
    best_fitness = min(tsp.bestFitnesses)
    avg_fitness = np.mean(tsp.avgFitnesses)
    log.append((key[i[0]], key[i[1]], round(best_fitness, 2), round(avg_fitness, 2)))
    tsp.plot("Total Distance", filename.split(".")[0])
    del tsp
    print("TSP completed with " + i[0] + " and " + i[1] + " selection schemes")
f.write("TSP")
for i in log:
    f.write(str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + "," + str(i[3]) + "\n")
f.close()
