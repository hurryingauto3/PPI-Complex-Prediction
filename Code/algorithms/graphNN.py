import torch
import torch.nn as nn
from torch_geometric.data import Data
import torch.nn.functional as F

from database.DatabaseOG import Database 
import networkx as nx

import torch_geometric.transforms as T
from torch_geometric.nn import GCNConv 
from torch_geometric.datasets import MNISTSuperpixels
from torch_geometric.loader import DataLoader
from torch_geometric.nn import global_mean_pool, graclus, max_pool, max_pool_x, GATConv, NNConv
from torch_geometric.utils import normalized_cut

# PPIDb = Database()
# # print("init database")
# # PPIDb.get_stats()
# # print("got stats")
# query = PPIDb.get_interactions_by_species("Saccharomyces cerevisiae")
# g = PPIDb.get_graph(query)

# def getTorchEdgelist(nxEdgeList):
#     edges = []
#     for i in nxEdgeList:
#         edge = [hash(i[0]), hash(i[1])]
#         edges.append(edge)
#         edges.append(edge[::-1])
#     return edges

# def getNodeFeatures(nxEdgeList):
#     features = []
#     for i in nxEdgeList:
#         features.append([0])
#     return features

# edge_index = torch.tensor(getTorchEdgelist(nx.to_edgelist(g)), dtype=torch.long)
# x = torch.tensor(getNodeFeatures(nx.to_edgelist(g)), dtype=torch.float)
# data = Data(x=x, edge_index=edge_index.t().contiguous())

transform = T.Cartesian(cat=False)
train_dataset = MNISTSuperpixels(".", True, transform=transform)
test_dataset = MNISTSuperpixels(".", False, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)
data = train_dataset

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)
data = data.to(device)

def normalized_cut_2d(edge_index, pos):
    row, col = edge_index
    edge_attr = torch.norm(pos[row] - pos[col], p=2, dim=1)
    return normalized_cut(edge_index, edge_attr, num_nodes=pos.size(0))
#Study
class MPNN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        nn1 = torch.nn.Sequential(torch.nn.Linear(2, 25), torch.nn.ReLU(),
                            torch.nn.Linear(25, data.num_features * 32))
        self.conv1 = NNConv(data.num_features, 32, torch.nn1, aggr='mean')

        nn2 = torch.nn.Sequential(torch.nn.Linear(2, 25), torch.nn.ReLU(),
                            torch.nn.Linear(25, 32 * 64))
        self.conv2 = NNConv(32, 64, nn2, aggr='mean')

        self.fc1 = torch.nn.Linear(64, 128)
        self.fc2 = torch.nn.Linear(128, data.num_classes)

    def forward(self, data):
        data.x = F.elu(self.conv1(data.x, data.edge_index, data.edge_attr))
        weight = normalized_cut_2d(data.edge_index, data.pos)
        cluster = graclus(data.edge_index, weight, data.x.size(0))
        data.edge_attr = None
        data = max_pool(cluster, data, transform=transform)

        data.x = F.elu(self.conv2(data.x, data.edge_index, data.edge_attr))
        weight = normalized_cut_2d(data.edge_index, data.pos)
        cluster = graclus(data.edge_index, weight, data.x.size(0))
        x, batch = max_pool_x(cluster, data.x, data.batch)

        x = global_mean_pool(x, batch)
        x = F.elu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        return F.log_softmax(self.fc2(x), dim=1)
#Study
# Neural net to generalize   convolution on graphs
class GCN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = GCNConv(data.num_node_features, 16)
        self.conv2 = GCNConv(16, 1)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)

        return F.log_softmax(x, dim=1)
#Study
class GAT(torch.nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()

        self.conv1 = GATConv(in_channels, 8, heads=8, dropout=0.6)
        # On the Pubmed dataset, use heads=8 in conv2.
        self.conv2 = GATConv(8 * 8, out_channels, heads=1, concat=False,
                             dropout=0.6)

    def forward(self, x, edge_index):
        x = F.dropout(x, p=0.6, training=self.training)
        x = F.elu(self.conv1(x, edge_index))
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=-1)

model = GCN().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

model.train()
for epoch in range(200):
    optimizer.zero_grad()
    out = model(data)
    loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()

model.eval()
pred = model(data).argmax(dim=1)
correct = (pred[data.test_mask] == data.y[data.test_mask]).sum()
acc = int(correct) / int(data.test_mask.sum())
print(f'Accuracy: {acc:.4f}')