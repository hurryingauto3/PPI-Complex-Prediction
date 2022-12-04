# Objectives 
1. Faster, higher-throughput algorithm whilst maintaining integrity in results. (Use biological + topological data to get results)
2. An easily accessible database with accurate data
3. Use of dynamic networks 
# Assumption 
1. All cliques are protien complexes but not all protien complexes are cliques 
2. If a protien complexe is not a clique then it is another topological structure, i.e. vertex cover, face cover, etc. 
3. Ensemble methode produce a more comprehensive results as they incorporate a larger amount of information.  
# General Definitions and Planning
### **Current Understanding of present work flow:**
1. Construct a database
    - a. Collect a large number of files containain PPIN data.
    - b. Methods to parse each file
    - c. Preprocess the data
    - d. Convert the preprocessed data extracted to a standardized file format
    - e. Method to read standardized file format
    - f. Establish a list of human protiens
    - e. Establish various useful metrics on these protiens.
    - g. Link this database to interaction database. 
2. Use PPIN to represent the dataset as networks 
3. Understand limitations of static networks, and how to overcome them using dynamic networks
4. Use topological and biological data to analyze the networks 
    - Topological algorithms
      - 1. Detecting cliques, other topological data structures.  
      - 2. Research how they are handling data and input.
    - Biological algorithms
      - 1. Needs more research -> Generally manipulating biological features of a complex.
      - 2. Research how they are handling data and input.
    - Esemble methods are using these methods in an arbitrary conjunction to produce more comprehensive results. 
5. Attempt to create methods for prediction of qualitative and quantitative information 
6. Verify the validity of the predicictions 
7. Establish the efficiency of the methods

Other possible tasks:

8. Use dynamic networks to visualize interactions in real time. 
9. Further work that is possible.



## PPI Networks
### Interactome
An interactome is a biological network the represents the whole set of molecular interactions in a specicied biological scope such as cell, an organism, etc. It specicifically referes to interactions amongst Protiens, between proteins and other small molecules, but it can also be used to refer to other interactions between other types of molecules, however for our usecase the term will strictly refer to interactions between proteins.
### PPI Networks
Protien-Protien Interaction Networks (PPIN) are mathematical representations of the physical interactions between proteins inside cells. These interactions are specific and hold biological meaning, and they occur within *binding regions*. Interactions can be *stable*, or *transient*. Stable interactions are, more or less, static while transient interactions serve specific temporary purposes which means they are dynamic. Therefore, a PPIN must be 1dynamic in order to represent

### Properties

- #### Small World Effect 
    
- #### Scale Free Network 
- #### Transivity 

### Analysis 

- #### Centrality 
- #### Closeness Centrality
- #### Betweenness Centrality
- #### Clustering Analysis

### Dataset
- Database of databases of PPIN
- http://www.vls3d.com/index.php/links/bioinformatics/protein-protein-interaction/ppi-databases-network
- http://www.string-db.org
- https://bet.uniprot.org
- https://sparql.uniprot.org 
- https://thebiogrid.org
- http://cicblade.dep.usal.es:8080/APID/init.action



