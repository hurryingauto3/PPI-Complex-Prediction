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
    fig = go.Figure(data=[edge_trace, node_trace, eweights_trace], layout=layout)
    return fig

def create_dashboard(server, PPIDb):
    """Create a Plotly Dash dashboard."""
    app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )
    
    G = nx.Graph()
    
    species = [x['Species Name'] for x in list(PPIDb.get_all_taxons(5))]
    
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
                    html.Button('Submit', 
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
            html.Div(id='container-button')
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
        State("species-variable", "value")
    )
    def update_graph(bttn_1, bttn_2, bttn_3, specie):
        changed_id = [p['prop_id'] for p in callback_context.triggered][0]
        if "clique_perc_button" in changed_id:
            query = PPIDb.get_interactions_by_species(specie)
            G = PPIDb.get_graph(query)
            cluster = [['RPOB', 'RPOC', 'RPSC', 'RPOA', 'YACL', 'YEEX', 'RPSG', 'RPSJ', 'RPSE', 'RPOZ', 'RPOD',
                        'RPLL', 'USG', 'GREA', 'HFQ', 'CARD', 'POLA', 'TOPA', 'MREB', 'CCPA', 'GROL', 'RPLA', 
                        'NUSG', 'P75093', 'RPSL', 'SIGA', 'HUPA', 'GREB', 'RPLD', 'NUSA', 'RPOH', 'RPOS', 'RAPA', 
                        'KDGR', 'CSPA', 'SSPA', 'RSD', 'RPON', 'CEDA', 'SSB', 'RPLB', 'GAPA', 'FECI', 'FLIA', 'YEGD'
                        , 'Q50312'], 
                    ['YCZI', 'TATC2', 'YCLI', 'FRUA', 'SWRC', 'YKOT', 'YKCC', 'YQFF', 'YDGH', 'TATC1', 'TATAC', 
                        'RACA', 'PPSC', 'YHAP', 'XHLA', 'YQBD', 'CSBC', 'FTSW', 'YOPZ', 'YWQJ', 'SMC', 'YDBI', 
                        'YTJP', 'TATAY', 'FLIZ', 'WPRA', 'XSEA', 'FTSA', 'MRED', 'YHGE', 'YTDP', 'YABT', 'YYXA', 
                        'YESS', 'CSSS', 'YDEL', 'ALBF', 'CTAB2', 'LIAS', 'FTSL', 'PBPB', 'DIVIB', 'CITS', 'YKJA', 
                        'SPOIIE', 'DIVIC', 'YQBO', 'YYAJ', 'PKSJ', 'YHAN', 'NHAK', 'YVBJ', 'YUAB', 'THYA2', 'CHEA', 
                        'YHDP', 'TATAD', 'YUEB', 'YVAQ', 'FTSH'], 
                    ['Q1CXR8', 'Q1DF43', 'Q1CWA4', 'Q1D1W0', 'Q1CVS0', 'Q1CWQ1', 'ASGD', 'Q1D8M1', 'Q1D4T4', 
                        'CHEB1', 'PHOR2', 'PHOP2', 'SDEK', 'Q1D4T3', 'Q1CYV2', 'Q1DCL6', 'Q1D6S6', 'Q1D1V9', 
                        'Q1DBP2', 'Q1D1K8', 'FRUA', 'Q1D948', 'Q1D6S5', 'PHOR1', 'PILR', 'Q1DBP1', 'Q1CZP2', 
                        'PILS', 'Q1D3G2', 'FRZS', 'AGLZ', 'Q1DCL7', 'Q1D033', 'Q1DD47', 'Q1CZP3', 'Q1D523', 
                        'PHOR3', 'Q1CZ93']]
            return draw_cluster_graph(G, cluster)
        elif "GA_button" in changed_id:
            query = PPIDb.get_interactions_by_species(specie)
            G = PPIDb.get_graph(query)
            return networkGraph(G)
        elif "specie_button" in changed_id:
            query = PPIDb.get_interactions_by_species(specie)
            G = PPIDb.get_graph(query)
            return networkGraph(G)
        else:
            G = nx.Graph()
            return networkGraph(G)

    return app.server