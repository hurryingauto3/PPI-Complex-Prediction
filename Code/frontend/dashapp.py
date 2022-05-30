
# G = nx.Graph(graph)
# pos = 

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import networkx as nx

Human_graph = {
        1 : {2 : {'weight': 6}, 3 : {'weight': 2}, 4 : {'weight': 8}},
        2 : {1 : {'weight': 6}},
        3 : {1 : {'weight': 2}},
        4 : {1 : {'weight': 8}}
    }

All_graph = {
        1 : {2 : {'weight': 6}, 3 : {'weight': 2}, 4 : {'weight': 8}},
        2 : {1 : {'weight': 6},},
        3 : {1 : {'weight': 2}},
        4 : {1 : {'weight': 8}, 5 : {'weight': 2}},
        5 : {4 : {'weight': 2}, 6 : {'weight': 3}},
        6 : {5 : {'weight': 3}}
    }

Biogrid_graph = {
        1 : {4 : {'weight': 8}},
        4 : {1 : {'weight': 8}, 5 : {'weight': 2}},
        5 : {4 : {'weight': 2}, 6 : {'weight': 3}},
        6 : {5 : {'weight': 3}}
    }


# Plotly figure
def networkGraph(G):
    # edges = [[EGDE_VAR, 'B'], ['B', 'C'], ['B', 'D']]
    # G = nx.Graph(graph)
    pos = nx.spring_layout(G)
    xtext=[]
    ytext=[]
    
    # edges trace
    edge_x = []
    edge_y = []
    etext = [f'{w}' for w in list(nx.get_edge_attributes(G, 'weight').values())]
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        xtext.append((x0+x1)/2)
        ytext.append((y0+y1)/2)
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(color='black', width=1),
        hoverinfo='none',
        showlegend=False,
        mode='lines')

    # edge label trace
    eweights_trace = go.Scatter(x=xtext,y= ytext, text = etext, mode='text',
                              marker_size=0.5,
                              textposition='top center',
                              hovertemplate='none')
    
    # nodes trace
    node_x = []
    node_y = []
    text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y, text=text,
        mode='markers+text',
        showlegend=False,
        hoverinfo='none',
        marker=dict(
            color='pink',
            size=50,
            line=dict(color='black', width=1)))

    # layout
    layout = dict(plot_bgcolor='white',
                  paper_bgcolor='white',
                  margin=dict(t=10, b=10, l=10, r=10, pad=0),
                  xaxis=dict(linecolor='black',
                             showgrid=False,
                             showticklabels=False,
                             mirror=True),
                  yaxis=dict(linecolor='black',
                             showgrid=False,
                             showticklabels=False,
                             mirror=True))

    # figure
    fig = go.Figure(data=[edge_trace, node_trace, eweights_trace], layout=layout)
    return fig

# Dash app

import dash_bootstrap_components as dbc
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Dash Networkx'

species = ['Human', 'All']
db = ['Biogrid', 'All']

controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Sort by Species"),
                dcc.Dropdown(
                    id="species-variable",
                    options=[
                        {"label": i, "value": i} for i in species
                    ],
                    value="All",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Sort by Database"),
                dcc.Dropdown(
                    id="db-variable",
                    options=[
                        {"label": i, "value": i} for i in db
                    ],
                    value="All",
                ),
            ]
        ),
        # html.Div(
        #     [
        #         dbc.Label("Cluster count"),
        #         dbc.Input(id="cluster-count", type="number", value=3),
        #     ]
        # ),
    ],
    body=True,
)

# app.layout = html.Div([
#         html.I('Write your EDGE_VAR'),
#         html.Br(),
#         dcc.Input(id='EGDE_VAR', type='text', value='K', debounce=True),
#         dcc.Graph(id='my-graph'),
#     ]
# )

app.layout = dbc.Container(
    [
        html.H1("Protein Interaction Graph"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="my-graph")),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

@app.callback(
    Output("my-graph", "figure"),
    [
        Input("species-variable", "value"),
        Input("db-variable", "value"),
    ],
)
def update_output(specie, db):
    if specie == 'All' or db == 'All':
        G = nx.Graph(All_graph)
    elif specie == 'Human':
        G = nx.Graph(Human_graph)
    else:
        G = nx.Graph(Biogrid_graph)
    return networkGraph(G)

if __name__ == '__main__':
    app.run_server()