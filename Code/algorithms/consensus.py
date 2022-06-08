

class Consensus:
    def __init__(self, clusters) -> None:
        self.clusters = clusters

    def IVC(self):
        pass

    def IPVC(self):
        pass

    def IPC(self):
        clusters = []
        for i in self.clusters[0]:
            cluster = []
            for j in self.clusters[1]:
                for k in set(i.nodes).intersection(set(j.nodes)):
                    cluster.append(k)
            clusters.append(cluster)
        return clusters
                    

                
