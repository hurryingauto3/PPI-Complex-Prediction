import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash import callback_context
import plotly.graph_objects as go
import networkx as nx
import dash_bootstrap_components as dbc
from dash import no_update
import itertools
import seaborn as sns
import numpy as np

def draw_cluster_graph(G, cluster_list):
    print("DRAWING CLUSTER GRAPH\n\n")
    palette = itertools.cycle([f'rgb{tuple((np.array(color)*255).astype(np.uint8))}' for color in sns.color_palette(None, len(cluster_list))])
    no_community = 'white'
    color_map = {}
    for cluster in cluster_list:
        color = next(palette)
        for node in cluster:
            color_map[node] = color
    
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
    master_color = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)
        if node in color_map.keys():
            master_color.append(color_map[node])
        else:
            master_color.append(no_community)

    node_trace = go.Scatter(
        x=node_x, y=node_y, text=text,
        mode='markers+text',
        showlegend=False,
        hoverinfo='none',
        marker=dict(
            color=master_color,
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
    print("FINISHED CLUSTER GRAPH\n")
    fig = go.Figure(data=[edge_trace, node_trace, eweights_trace], layout=layout)
    return fig

def networkGraph(G):
    print("DRAWING NETWORK GRAPH\n\n")
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
    print("FINISHED NETWORK GRAPH\n")
    fig = go.Figure(data=[edge_trace, node_trace, eweights_trace], layout=layout)
    return fig

def create_dashboard(server, master):
    """Create a Plotly Dash dashboard."""
    app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )
    
    G = nx.Graph()
    
    species = [x['Species Name'] for x in list(master.get_taxons(30))]
    
    controls = dbc.Card(
        [
            html.Div(
                [
                    dbc.Label("Filter by Species"),
                    dcc.Dropdown(
                        id="species-variable",
                        options=[
                            {"label": i, "value": i} for i in species
                        ],
                        value=species[0],
                    ),
                ]
            ),
            html.Div(
                [
                    html.Button('Filter', 
                                id = 'specie_button', 
                                n_clicks = 0),
                ]
            ),
            html.Div(
                [
                    html.Button('Clique percolation', 
                                id = 'clique_perc_button', 
                                n_clicks = 0),
                    
                    html.Button('Genetic Algorithm', 
                                id = 'GA_button', 
                                n_clicks = 0),
                ]
            ),
            html.Div(
                html.Div(
                [
                    html.Button('Apply Consensus', 
                                id = 'consensus_button', 
                                n_clicks = 0),
                ]
            ),    
            ),
        ],
        body=True,
    )
    
    # Create Dash Layout
    app.layout = dbc.Container(
        [
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
        Input("clique_perc_button", "n_clicks"),
        Input("GA_button", "n_clicks"),
        Input("specie_button", "n_clicks"),
        Input("consensus_button", "n_clicks"),
        State("species-variable", "value")
    )
    def update_graph(bttn_1, bttn_2, bttn_3, bttn_4, specie):
        changed_id = [p['prop_id'] for p in callback_context.triggered][0]
        if "clique_perc_button" in changed_id:
            print("pressed clique button")
            master.add_perc_for_specie(specie)
            clusters = master.get_specie_cluster_nodes(specie, 'cliqueperc')
            G = master.get_specie_cluster_graph(specie, 'cliqueperc')
            return draw_cluster_graph(G, clusters)
        elif "GA_button" in changed_id:
            print("pressed GA button")
            print('starting GA')
            master.add_gen_for_specie(specie)
            print('completed GA')
            clusters = master.get_specie_cluster_nodes(specie, 'genalgo')
            G = master.get_specie_cluster_graph(specie, 'genalgo')
            return draw_cluster_graph(G, clusters)
        elif "specie_button" in changed_id:
            print("pressed filter button")
            G = master.get_specie_interactions(specie)
            return networkGraph(G)
        elif "consensus_button" in changed_id:
            print("pressed consensus button")
            # G = master.get_consensus(specie)
            G = nx.Graph()
            return networkGraph(G)
        else:
            print("done nothing yet")
            G = nx.Graph()
            return networkGraph(G)

    return app.server