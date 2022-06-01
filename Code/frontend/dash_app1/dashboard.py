import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import networkx as nx
import dash_bootstrap_components as dbc


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

def create_dashboard(server, PPIDb):
    """Create a Plotly Dash dashboard."""
    app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    species = [specie['Species Name'] for specie in list(PPIDb.get_all_taxons(5))]
    species.insert(0, 'All')
    db = ['All', 'BioGrid', 'Mentha', 'MINT']
    
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
    
    # species = ['Human', 'All']
    # db = ['Biogrid', 'All']
    
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
        ],
        body=True,
    )
    
    # Create Dash Layout
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
        elif specie == 'Homo sapiens':
            G = nx.Graph(Human_graph)
        else:
            G = nx.Graph(Biogrid_graph)
        return networkGraph(G)
    
    # init_callbacks(dash_app, Human_graph, All_graph)

    return app.server

# def init_callbacks(dash_app, Human_graph, All_graph):
    # @dash_app.callback(
    #     Output("my-graph", "figure"),
    #         [
    #             Input("species-variable", "value"),
    #             Input("db-variable", "value"),
    #         ],
    # )
    # def update_output(specie):
    #     if specie == 'All':
    #         G = nx.Graph(All_graph)
    #     else:
    #         G = nx.Graph(Human_graph)
    #     return networkGraph(G)
        
# Plotly figure