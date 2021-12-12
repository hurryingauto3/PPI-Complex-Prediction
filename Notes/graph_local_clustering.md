## [Protein Complex Identification by Supervised Graph Local Clustering](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2718642/)

### Abstract 

#### Motivation

Given a graph representing protein interaction data, we can search for subgraphs representing
protein complexes. It has been previously assumed that complexes form cliques, but this 
generalization does not hold for all complexes. New algorithms are needed that use other 
topological structures. 

#### Results 

The paper presents an algorithm to infer protein complexes from weighted interaction graphs, 
using graph topological patterns and biological properties. Each complex subgraph is 
modelled using a probabilistic Bayesian network (BN). A training set of known 
complexes is used to learn the parameters of the BN. The algorithm achieves a considerable 
improvement over other clique-based algorithms. 

### Introduction

Problems:
- High-throughput experimental approaches  suffer from high false positive and false negative rates
- Mass spectrometry can miss complexes, tagging disturbs complex formation and they can escape detection 

Previous attempts at automatic complex identification used binary protein-interaction graphs, and methods used unsupervised graph clustering. 

Five categories for automatic complex identification:
1. Graph segmentation: Partitioning the nodes of a given graph into distinct clusters using cost-based local search algorithm. Zotenko proposed a graph-theoretical approach to identify functional groups. 
2. Overlapping clustering: Some proteins participate in multiple complexes - overlapping clusters, detect densely connected regions in large PPI networks using local neighborhood density. 
3. New similarity measures: cluster similarity is calculated using the vectors of nodes' attributes.
4. Conservation across species: Using conversation alignment to find complexes common to species. Sharan et. al. did so with yeast and bacteria. 
5. Spatial constraints analysis: utilize spatial aspects of complex formation. Can utilize mass spectrometry complex data and Y2H binary interaction data.

Other topological structures could represent a complex in a PPI graph. For example, "star" or 
"spoke" model, in which vertices connect to a 'Bait' protein. Another structure could be one that links several small densely connected components with loose linked edges.
The paper presents a probabilistic algorithm that has significantly better F1-scores and overall results compared to other approaches.

### Methods 

Other features can characterize complexes, for example, biological, chemical or physical properties. Incorporating these features into supervised learning can help identify new complexes.

The input to the proposed algorithm is a weighted graph of interacting proteins. The vertices represent proteins and the edges represent interactions and edge weights represent likelihood of interaction. 

#### Complex Features 

Feature extraction is an important problem. The authors used 33 features extracted from 10 groups that included topological measurements and biological data of the group of proteins in the subgraph such as node size, graph density, degree statistics, clustering coefficient statistics, first eigenvalues, etc.

Possible biological data that we can use: protein size and protein weight


#### A Supervised Bayesian Network (BN) to Model Complexes

The authors assume a generative probabilistic model for complexes. Features are generated based on two parameters: whether a subgraph is complex or not $C$, and the number of nodes in 
the subgraph $N$. The larger the complex the more unlikely it is that all members interact 
with one another. Some features depend on $N$. For a subgraph in a PPI network, the conditional probability of how likely it represents a complex is given using an equation that uses 
Bayes Rule, the chain rue and conditional independence that is used to decompose 
the probability to products of different features. Using this posterior, we can compute 
log likelihood ratio for each candidate subgraph.

Different techniques used:
- Bayes' rule 
- Log likelihood ratios
- Maximum likelihood estimation (for learning conditional dependencies)
- Multinomial distribution 
- Bayesian Beta Prior (for smoothing multinomial parameters)

#### Searching for New Complexes

Searching for maximally sc
oring subgraphs in PPI graph is NP-hard, which means there are no 
efficient polynomial time algorithms to do so. The paper uses iterated simulated annealing (ISA) search and used the complex ratio score as the objective function. 

The Algorithm:

**Input**:
	- Weighted PPI matrix;
	- A training set of complexes and non-complexes 

**Output**:
	- Discovered list of protein complexes;

**Complex model parameter estimation**:
	- Extract property features from positive and negative training examples 
	- Discretize the continuous features;
	- Calculate the BN MLE parameters for different features properties on the multinomial distribution;

**Search for complexes**:
	- Starting from the seeding subgraphs, apply simulated annealing search to expand and identify candidate complexes;
	- Output subgraphs with ratios exceeding a certain threshold


### Experiments and Results 

#### Performance measures 

The authors defined three descriptors for each pair of a known and predicted complex:
- A: number of proteins only in the predicted complex 
- B: number of proteins only in the known complex 
- C: number of proteins in the overlap between two 

A predicted complex recovers a known complex if:
$\frac{C}{A+C} > p$ and $\frac{C}{B+C} > p$ 
where $p$ is an input parameter between 0 and 1.

The paper used precision, recall and F1 scores to evaluate complex identification.
Generally better performance compared to other pre-existing algorithms.


### Conclusion 

The algorithm proposed does not rely on the dense assumption of complex subgraphs, and integrates 
subgraph topologies and biological evidence and learns these features from known complexes. This allows the algorithm to detect complexes missed by previous algorithms and also achieve better precision and recall scores.

We can add other topological properties and other types of features to this framework such as other topological patterns, or protein function information. This algorithm can also be applied to 
other species whose protein interaction data has been made recently available.
