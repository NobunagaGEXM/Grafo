import json
import networkx as nx
import dash
from dash import Dash, html, Input,State, Output, callback, dcc,Patch
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from collections import deque
app = Dash(__name__)
G = nx.Graph()
orientado = False
ponderado = False
ltape = []
ltapn = []
G.add_node(0)
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)
G.add_edge(0,1)
G.add_edge(1,2)
G.add_edge(0,3)
G.add_edge(3,4)
G.add_edge(4,5)
G.add_edge(2,5)
G.add_edge(1,4)



p =-1
def dfs(G,start):
    c={}
    pi={}
    d={}
    f={}
    for u in G.nodes():
        c[u]="Branco"
        pi[u]=None
        d[u]=None
        f[u]=None
    tempo=0
    edges_visited = []
    aux = len(G.nodes())
    if c[int(start)]=="Branco":
        tempo=dfs_visit_aula(G,int(start),c,pi,d,f,tempo)
    for u in G.nodes():
        if c[u]=="Branco":
            tempo=dfs_visit_aula(G,u,c,pi,d,f,tempo)
    aux -= 1
    while aux != -1:
        if pi[aux] != None:
            edges_visited.append((pi[aux],aux))
        aux = aux - 1
    return edges_visited

def dfs_visit_aula(G,u,c,pi,d,f,tempo):
    tempo=tempo+1
    d[u]=tempo
    c[u]="Cinza"
    for v in G.adj[u]:
        if c[v]=="Branco":
            pi[v]=u
            tempo=dfs_visit_aula(G,v,c,pi,d,f,tempo)
    c[u]="Preto"
    tempo=tempo+1
    f[u]=tempo
    return tempo


def bfs(grafo, start, end,parent):
    visited = []
    queue = [start]
    edges_visited = set()
    while queue:
        vertex = int(queue.pop(0))
        if vertex not in visited:
            visited.append(vertex)
            if isinstance(grafo, nx.DiGraph):
                if grafo.successors(vertex):
                    neighbors = grafo.successors(vertex) 
            else:
                neighbors = grafo.neighbors(vertex)
            for neighbor in neighbors:
                if neighbor not in visited and grafo.get_edge_data(int(vertex),int(neighbor))['weight'] > 0:
                    queue.append(neighbor)
                    if isinstance(grafo, nx.DiGraph):
                        edges_visited.add((vertex, neighbor))
                    else:
                        edges_visited.add((vertex, neighbor))
                        edges_visited.add((neighbor, vertex))
                if  int(neighbor) == int(end) and vertex != parent and grafo.get_edge_data(int(vertex),int(neighbor))['weight'] > 0:
                    return True
    return False

def bfs3(grafo, start):
    visited = []
    queue = [start]
    edges_visited = set()
    while queue:
        vertex = int(queue.pop(0))
        if vertex not in visited:
            visited.append(vertex)
            if isinstance(grafo, nx.DiGraph):
                if grafo.successors(vertex):
                    neighbors = grafo.successors(vertex) 
            else:
                neighbors = grafo.neighbors(vertex)
            for neighbor in neighbors:
                if neighbor not in visited and neighbor not in queue:
                    queue.append(neighbor)
                    if isinstance(grafo, nx.DiGraph):
                        edges_visited.add((vertex, neighbor))
                    else:
                        edges_visited.add((vertex, neighbor))
                        edges_visited.add((neighbor, vertex))
    return edges_visited

def bfs2(grafo, start, end,parent):
    visited = []
    queue = [start]
    edges_visited = set()
    while queue:
        vertex = int(queue.pop(0))
        if vertex not in visited:
            visited.append(vertex)
            if isinstance(grafo, nx.DiGraph):
                if grafo.successors(vertex):
                    neighbors = grafo.successors(vertex) 
            else:
                neighbors = grafo.neighbors(vertex)
            for neighbor in neighbors:
                if neighbor not in visited and neighbor not in queue:
                    queue.append(neighbor)
                    if isinstance(grafo, nx.DiGraph):
                        edges_visited.add((vertex, neighbor))
                    else:
                        edges_visited.add((vertex, neighbor))
                        edges_visited.add((neighbor, vertex))
                if  int(neighbor) == int(end) and vertex != parent and grafo.get_edge_data(int(vertex),int(neighbor))['weight'] > 0:
                    return vertex
    return -1

def ford_fulkerson(G3, start_node, end_node):
    parent= -1
    max_flow = 0
    for i, j in G3.edges():
        if 'flow' not in G3[i][j]:
            G3[i][j]['flow'] = 0

    while bfs( G3,start_node, end_node, parent):
        path = []
        parente = bfs2( G3,start_node, end_node, parent)
        parent = parente
        path_flow = float('Inf')
        current_node = end_node
        path.append(current_node)
        while int(current_node) != int(start_node):
            aux =G3.get_edge_data(int(parent),int( current_node))['weight']
            if aux:
                path_flow = min(path_flow, int(aux) )
            else:
                path_flow = 0
            current_node = parent
            path.append(parent)
            prede = list(G3.predecessors(parent))
            if(len(prede)>0):
                i = 0
                for p in prede:
                    aux =G3.get_edge_data(int(p),int(parent))['weight']
                    if 0<aux:
                        parent = p
                        i = 1
                if i == 0:
                    current_node = start_node
                    path_flow = 0
        max_flow += path_flow
        current_node = end_node
        parent = parente
        c = 1
        while int(current_node) != int(start_node):
            G3[int(parent)][int(current_node)]['weight'] -= path_flow
            G3[int(parent)][int(current_node)]['flow'] += path_flow
            current_node = parent
            if int(current_node) != int(start_node):
                parent = prede[c]
                c+=1

            
    return max_flow


nodes = [
    {
        'data': {'id': id, 'label': name},
        'position': {'x': 20*x, 'y': -20*y}
    }
    for id, name, x, y in (
        ('0', '0', 1, 1),
        ('1', '1', 1, 1),
        ('2', '2', 2, 2),
    )
]
default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)'
        },},{
        'selector': 'edge',
                'style': {
                    'curve-style': 'bezier',
                    'label': 'data(weight)'
                }
    }
]
ori_stylesheet = [
            # Group selectors
            {
                'selector': 'node',
                'style': {
                    'background-color': '#BFD7B5',
                    'label': 'data(id)'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    # The default curve style does not work with certain arrows
                    'curve-style': 'bezier',
                    'target-arrow-color': 'black',
                    'target-arrow-shape': 'triangle',
                    'label': 'data(weight)'
                }
            },
        ]
edges = [
    {'data': {'source': source, 'target': target}}
    for source, target in (
        ('0', '1'),
        ('1', '2'),
    )
]

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'padding': '10px',
        'width': '100%', 'height': '50px',
        'overflow':'scroll'
    },
    'pre2': {
        'padding': '10px',
    }
}
app.layout = html.Div([
    html.Div([
        html.Pre(id='dataG', style=styles['pre2']),
        cyto.Cytoscape(
        id='cytoscape-event-callbacks-1',
        layout={'name': 'cose'},
        elements=nodes + edges,
        stylesheet=default_stylesheet,
        style={'width': '100%', 'height': '450px'},
        minZoom=0.5,
        maxZoom=1.5,
        zoomingEnabled=True,
        userZoomingEnabled=True,
    )
    ],style={'border': 'thin lightgrey solid'}),
    
    
    html.Div([
        html.Button('Criar No', id='btn-add-node', n_clicks=0),
        html.Button('Remover No', id='btn-remove-node', n_clicks=0),
        html.Button("Criar aresta", id='btn-add-edge', n_clicks=0),
        html.Button("Remover aresta", id='btn-remove-edge', n_clicks=0),
        html.Button("mudar grafo para orientado ou não", id='btn-ori-edge', n_clicks=0),
        html.Button("mudar grafo para ponderado ou não", id='btn-pon', n_clicks=0),
        html.Div([
            dcc.Input(id='input-on-submit-text', type='text'),
            html.Button("Alterar peso da aresta", id='btn-change-edge',n_clicks = 0),]),
        html.Div([
            html.Button("bfs", id='btn-bfs', n_clicks=0),
            html.Button("dfs", id='btn-dfs', n_clicks=0),
            html.Button("fluxo", id='btn-fluxo', n_clicks=0)
        ]),
]), 
html.Div([
    html.Pre(id='cytoscape-tapNodeData-json', style=styles['pre']),
    html.Pre(id='cytoscape-tapEdgeData-json', style=styles['pre']),
    html.Pre(id='result', style=styles['pre']),
])
    
])

@callback(Output('cytoscape-tapNodeData-json', 'children'),
              Input('cytoscape-event-callbacks-1', 'tapNode'),
              prevent_initial_call=True)
def displayTapNodeData(node):
    global ltapn
    if node not in ltapn:
        ltapn.append(node['data'])
        return json.dumps(node['data'], indent=2)
    return json.dumps(node, indent=2)

@callback(Output('cytoscape-tapEdgeData-json', 'children'), 
              Input('cytoscape-event-callbacks-1', 'tapEdge'))
def displayTapEdgeData(edge):
    global ltape
    if edge != None:
        if edge['data'] not in ltape:
            ltape.append(edge['data'])
        return json.dumps(edge['data'], indent=2)
    return json.dumps(edge, indent=2)

@callback(Output('cytoscape-event-callbacks-1', 'elements'),
            Output('cytoscape-event-callbacks-1', 'stylesheet'),
            Output('dataG','children'),
            Output('result','children'),
              Input('btn-add-node', 'n_clicks'),
              Input('btn-remove-node', 'n_clicks'),
              Input('btn-add-edge', 'n_clicks'),
              Input('btn-remove-edge', 'n_clicks'),
              Input('btn-change-edge', 'n_clicks'),
              Input('btn-ori-edge', 'n_clicks'),
              Input('btn-pon', 'n_clicks'),
              Input('btn-fluxo','n_clicks'),
              Input('btn-bfs','n_clicks'),
              Input('btn-dfs','n_clicks'),
              Input('cytoscape-event-callbacks-1', 'tapNode'),
              State('input-on-submit-text', 'value'),
              State('cytoscape-event-callbacks-1', 'elements'),
              State('cytoscape-event-callbacks-1', 'stylesheet'),
              State('result','children'),
              prevent_initial_call=True
)
def ChangeData(n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,value,m,sty,chil):
    global ltapn,ltape,G,orientado,default_stylesheet,ori_stylesheet,ponderado
    flag = False
    flag1 = False
    flag2 = False
    result = []
    pon = " nao ponderado "
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if prop_id == 'btn-add-node':
            G.add_node(int(n1))
        if prop_id == 'btn-remove-node':
            G.remove_node(int(ltapn[-1]['id']))
            ltapn.pop
        if prop_id == 'btn-add-edge':
            if len(ltapn) > 1:
                if ponderado:
                    G.add_edge(int(ltapn[-2]['id']),int(ltapn[-1]['id']),weight=int(1))
                else:
                    G.add_edge(int(ltapn[-2]['id']),int(ltapn[-1]['id']))
                ltapn = []
        if prop_id == 'btn-remove-edge':
            if len(ltape) > 0:
                G.remove_edge(int(ltape[-1]['source']),int(ltape[-1]['target']))
                ltape = []
        if prop_id == 'btn-ori-edge':
            if orientado:
                orientado = False
            else:
                orientado = True
            nodes = G.nodes(data=True)
            edges = G.edges(data=True)
            if orientado: 
                novo_G = nx.DiGraph()
            else:
                novo_G = nx.Graph()
            novo_G.add_nodes_from(nodes)
            novo_G.add_edges_from(edges)

            G = novo_G
        if prop_id == 'btn-change-edge':
            if ponderado == False:
                ponderado = True
            edge = [int(ltape[-1]['source']),int(ltape[-1]['target'])]
            if edge in G.edges():
                G.remove_edge(edge[0],edge[1])
                G.add_edge(edge[0],edge[1],weight=int(value))
                for i, j in G.edges():
                    if (i, j) != edge:
                        if 'weight' not in G[i][j]:
                            G.remove_edge(i,j)
                            G.add_edge(i,j,weight=int(1))
        if prop_id == 'btn-pon':
            if ponderado:
                ponderado = False
            else:
                ponderado = True
            if ponderado:
                for i, j in G.edges():
                    if 'weight' not in G[i][j]:
                        G[i][j]['weight'] = int(1)
            else:
                for node, edges in nx.to_dict_of_dicts(G).items():
                    for edge, attrs in edges.items():
                        attrs.pop('weight', None)
        n_sty = ''
        if prop_id == 'btn-fluxo':
            flag = True
            res_g = nx.DiGraph()
            res_g = G.copy()
            result = ford_fulkerson(res_g,ltapn[-2]['id'],ltapn[-1]['id'])
            start_node = ltapn[-2]['id']
            end_node = ltapn[-1]['id']
        if prop_id == 'btn-bfs':
            flag1 = True
            res_g = nx.DiGraph()
            res_g = G.copy()
            ee = bfs3( res_g,ltapn[-1]['id'])
            ed = f"{ee}"
            result =  json.dumps(ed, indent=2)
            start_node = ltapn[-1]['id']
        if prop_id == 'btn-dfs':
            flag2 = True
            res_g = nx.DiGraph()
            res_g = G.copy()
            ee = dfs( res_g,int(ltapn[-1]['id']))
            ed = f"{ee}"
            result =  json.dumps(ed, indent=2)
            start_node = ltapn[-1]['id']
            
    elementos = []
    if orientado:
        ori = " orientado "
        n_sty = [
            # Group selectors
            {
                'selector': 'node',
                'style': {
                    'background-color': '#BFD7B5',
                    'label': 'data(id)',
                    'text-halign':'center',
                    'text-valign':'center',
                }
            },
            {
                'selector': 'edge',
                'style': {
                    # The default curve style does not work with certain arrows
                    'curve-style': 'bezier',
                    'target-arrow-color': 'black',
                    'target-arrow-shape': 'triangle',
                    'label': 'data(weight)',
                }
            },
        ]
    else:
        ori = " nao orientado "
        n_sty = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#BFD7B5',
            'label': 'data(label)',
            'text-halign':'center',
            'text-valign':'center',
        },},{
        'selector': 'edge',
                'style': {
                    'curve-style': 'bezier',
                    'label': 'data(weight)'
                }
    }
]
    if flag:
        for edge in res_g.edges:
            elementos += [{'data': {'id': f"{node}", 'label': f"{node}"}} for node in res_g.nodes()] + \
                   [{'data': {'id': f"{edge[0]}-{edge[1]}", 'source': f"{edge[0]}", "target": f"{edge[1]}", 'weight': str(res_g.get_edge_data(edge[0], edge[1])['weight']) + ',' + str(res_g.get_edge_data(edge[0], edge[1])['flow'])}}]
        n_sty += [
                    {
                        'selector': f'node[id="{start_node}"]',
                        'style': {
                            'background-color': 'blue'
                        }
                    }
                ]
        n_sty += [
                    {
                        'selector': f'node[id="{end_node}"]',
                        'style': {
                            'background-color': 'red'
                        }
                    }
                ]
        if isinstance(res_g, nx.DiGraph):                
                    n_sty += [
                    {
                        'selector': f'edge[id="{edge[0]}-{edge[1]}"]',
                        'style': {
                            'line-color': 'red',
                            'width': 3,
                            'weight':f'{res_g.get_edge_data(edge[0], edge[1])["weight"]}'+','+f'{res_g.get_edge_data(edge[0], edge[1])["flow"]}',
                        }
                    } for edge in res_g.edges
                    ]
        flag = False
    elif flag1:
        if ponderado:
            pon = " ponderado "
            elementos = [{'data': {'id': f"{node}", 'label': f"{node}"}} for node in res_g.nodes()] + \
                   [{'data': {'id': f"{edge[0]}-{edge[1]}", 'source': f"{edge[0]}", "target": f"{edge[1]}", 'weight': str(G.get_edge_data(edge[0], edge[1])['weight'])}} for edge in res_g.edges()]
        else:
            pon = " nao ponderado "
            elementos = [{'data': {'id': f"{node}", 'label': f"{node}"}} for node in res_g.nodes()] + \
                   [{'data': {'id': f"{edge[0]}-{edge[1]}", 'source': f"{edge[0]}", "target": f"{edge[1]}", 'weight': ''}} for edge in res_g.edges()]
        n_sty += [
                    {
                        'selector': f'node[id="{start_node}"]',
                        'style': {
                            'background-color': 'blue'
                        }
                    }
                ]              
        n_sty += [
                    {
                        'selector': f'edge[id="{edge[0]}-{edge[1]}"]',
                        'style': {
                            'line-color': 'red',
                            'width': 3,
                        }
                    } for edge in ee
                    ]
        flag1 = False
    elif flag2:
        if ponderado:
            pon = " ponderado "
            elementos = [{'data': {'id': f"{node}", 'label': f"{node}"}} for node in res_g.nodes()] + \
                   [{'data': {'id': f"{edge[0]}-{edge[1]}", 'source': f"{edge[0]}", "target": f"{edge[1]}", 'weight': str(G.get_edge_data(edge[0], edge[1])['weight'])}} for edge in res_g.edges()]
        else:
            pon = " nao ponderado "
            elementos = [{'data': {'id': f"{node}", 'label': f"{node}"}} for node in res_g.nodes()] + \
                   [{'data': {'id': f"{edge[0]}-{edge[1]}", 'source': f"{edge[0]}", "target": f"{edge[1]}", 'weight': ''}} for edge in res_g.edges()]
        n_sty += [
                    {
                        'selector': f'node[id="{start_node}"]',
                        'style': {
                            'background-color': 'blue'
                        }
                    }
                ]              
        n_sty += [
                    {
                        'selector': f'edge[id="{edge[0]}-{edge[1]}"]',
                        'style': {
                            'line-color': 'red',
                            'width': 3,
                        }
                    } for edge in ee
                    ]
        flag2 = False
    else:
        if ponderado:
            pon = " ponderado "
            elementos = [{'data': {'id': f"{node}", 'label': f"{node}"}} for node in G.nodes()] + \
                   [{'data': {'id': f"{edge[0]}-{edge[1]}", 'source': f"{edge[0]}", "target": f"{edge[1]}", 'weight': str(G.get_edge_data(edge[0], edge[1])['weight'])}} for edge in G.edges()]
        else:
            pon = " nao ponderado "
            elementos = [{'data': {'id': f"{node}", 'label': f"{node}"}} for node in G.nodes()] + \
                   [{'data': {'id': f"{edge[0]}-{edge[1]}", 'source': f"{edge[0]}", "target": f"{edge[1]}", 'weight': ''}} for edge in G.edges()]
    dados = json.dumps('Grafo'+f'{ori}'+f'{pon}'+' com '+f'{len(G.nodes)}'+' nos e '+f'{len(G.edges)}'+' arestas')
    return elementos,n_sty,dados,result

if __name__ == '__main__':
    app.run(debug=True)