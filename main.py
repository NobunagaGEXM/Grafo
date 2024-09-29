import json
import networkx as nx
from dash import Dash, html, Input,State, Output, callback, dcc,Patch
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
app = Dash(__name__)
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll',
        'padding': '10px',
        'width': '100%', 'height': '50px'
    },
    'pre2': {
        'border': 'thin lightgrey solid',
        'padding': '10px',
    }
}
def dfs_aula(G):
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
    for u in G.nodes():
        if c[u]=="Branco":
            tempo=dfs_visit_aula(G,u,c,pi,d,f,tempo)
    return c,pi,d,f

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

def bfs_aula(G,s):
    c ={}
    d ={}
    pi ={}
    o={}
    edges_colored = []
    for u in G.nodes():
        c[u]="Branco"
        d[u]=None
        pi[u]=None
    c[s]="Cinza"
    d[s]=0
    pi[s]=None  
    Q=[s]
    x=1
    while Q:
        u=Q.pop(0)
        o[x]=u
        x=x+1
        for v in G.adj[u]:
            if G.is_directed:
                if c[v]=="Branco" and G.has_edge(u,v):
                    c[v]="Cinza"
                    d[v]=d[u]+1
                    pi[v]=u
                    Q.append(v)
                    edges_colored.append((u,v))
            else:
                if c[v]=="Branco":
                    c[v]="Cinza"
                    d[v]=d[u]+1
                    pi[v]=u
                    Q.append(v)
                    edges_colored.append((u,v))
                    edges_colored.append((v,u))
        c[u]="Preto"
    return o,d,pi,edges_colored
G = nx.Graph()
G.add_node('0')
G.add_edge('0','0')
nodes = [
    {
        'data': {'id': id, 'label': name},
        'position': {'x': 20*x, 'y': -20*y}
    }
    for id, name, x, y in (
        ('0', '0', 1, 1),
    )
]

edges = [
    {'data': {'source': source, 'target': target}}
    for source, target in (
        ('0', '0'),
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
style_edge = [
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
                    'line-color': 'black',
                    'label': 'data(weight)'
                }
            },
        ]
clicksaddn = 0
clicksrevn = 0
clicksaddne = 0
clicksori = 0
clicksrevne = 0
clickschae = 0
clicksbfs = 0
clicksdfs = 0
clicksload = 0
clickssav = 0
ori = False
ltap = nodes[0]['data']
lltap = nodes[0]['data']
ltape = edges[0]['data']
file = open('saves.txt', 'r')
saves = file.read()
file.close()
lists = saves
ida = 0 


app.layout = html.Div([
    html.Div([
        cyto.Cytoscape(
        id='cytoscape-event-callbacks-1',
        layout={'name': 'cose'},
        elements=edges+nodes,
        stylesheet=default_stylesheet,
        style={'width': '100%', 'height': '450px','border': 'thin lightgrey solid'},
        minZoom=0.5,
        maxZoom=1.5,
        zoomingEnabled=True,
        userZoomingEnabled=True,
    ),
    ]),
    
    
    html.Div([
        html.Button('Criar No', id='btn-add-node', n_clicks=0),
        html.Button('Remover No', id='btn-remove-node', n_clicks=0),
        html.Button("Criar aresta", id='btn-add-edge', n_clicks=0),
        html.Button("mudar grafo para orientado ou não", id='btn-ori-edge', n_clicks=0),
        html.Button("Remover aresta", id='btn-remove-edge', n_clicks=0),
        html.Div([
            dcc.Input(id='input-on-submit-text', type='text'),
            html.Button("Alterar peso da aresta", id='btn-change-edge',n_clicks = 0),]),
        html.Div([
            html.Button("bfs", id='btn-bfs', n_clicks=0),
            html.Button("dfs", id='btn-dfs', n_clicks=0),
            html.Button("update", id='upd', n_clicks=0)
        ]),
        html.Div([ 
            dcc.Input(id='input-on-submit-text-save', type='text'),
            html.Button("save", id='save', n_clicks=0),
            html.Pre([
                dcc.Dropdown([saves.split(',')[i] for i in range(len(saves.split(','))) if saves.split(',')[i] != ''],'a',id = 'bar'),
                html.Br()
            ],id='all'),
            html.Button("load", id='load', n_clicks=0)
        ])
]), 
html.Div([
    html.Pre(id='cytoscape-tapNodeData-json', style=styles['pre']),
    html.Pre(id='cytoscape-tapEdgeData-json', style=styles['pre']),
    html.Pre(id='dataG', style=styles['pre']),
    html.Pre(id='result', style=styles['pre']),
])
    
])


@callback(Output('cytoscape-tapNodeData-json', 'children'),
              Input('cytoscape-event-callbacks-1', 'tapNode'),
              prevent_initial_call=True)
def displayTapNodeData(node):
    global ltap,lltap
    if node != None:
        lltap = ltap
        if ltap != node['data']:
            ltap = node['data']
        return json.dumps(node['data'], indent=2)
    return json.dumps(node, indent=2)

@callback(Output('dataG', 'children'),
              Input('cytoscape-event-callbacks-1', 'tapNode'),
              Input('cytoscape-event-callbacks-1', 'tapEdge'),
              prevent_initial_call=True)
def displayG(_,__):
    global G,ori
    if G != None:
        if ori:
            return str(G)+" orientado"
        return str(G)+" não orientado"

@callback(Output('cytoscape-tapEdgeData-json', 'children'), 
              Input('cytoscape-event-callbacks-1', 'tapEdge'))
def displayTapEdgeData(edge):
    global ltape
    if edge != None:
        if ltape != edge['data']:
            ltape = edge['data']
        return json.dumps(edge['data'], indent=2)
    return json.dumps(edge, indent=2)

@callback(Output('cytoscape-event-callbacks-1', 'elements', allow_duplicate=True),
              Input('btn-add-node', 'n_clicks'),
              Input('btn-remove-node', 'n_clicks'),
              Input('btn-add-edge', 'n_clicks'),
              Input('btn-remove-edge', 'n_clicks'),
              Input('btn-change-edge', 'n_clicks'),
              State('input-on-submit-text', 'value'),
              State('cytoscape-event-callbacks-1', 'elements'),
              prevent_initial_call=True
)
def ChangeData(n1,n2,n3,n4,n5,value,m):
    global ida,nodes,edges,x,y,clicksrevn,clicksaddn,G,clicksaddne,clicksrevne,clickschae
    global ltap,lltap,ltape
    if n1 > clicksaddn:
        clicksaddn = n1
        ida += 1
        G.add_node(str(ida))
        x=1
        y=1
        nodes.append({
            'data': {'id': str(ida), 'label': str(ida)},
            'position': {'x': x, 'y': y}
        })
        return nodes+edges
    if n2 > clicksrevn:
        clicksrevn = n2
        aux = None
        for i in G.edges:
            if ltap['id'] in i:
                G.remove_edge(i[0],i[1])
        for i in G.nodes:
            if i == ltap['id']:
                aux = i
        if aux != None:
            G.remove_node(aux)           
        for i in nodes:
            if i['data']['id'] == ltap['id']:
                nodes.remove(i)
        for i in edges:
            if i['data']['source'] == ltap['id']:
                edges.remove(i)
        for i in edges:
            if i['data']['target'] == ltap['id']:
                edges.remove(i)
        return nodes+edges
    if n3 > clicksaddne:
        clicksaddne = n3
        G.add_edge(ltap['id'],lltap['id'])
        edges.append({
        'data': {'source': lltap['id'], 'target': ltap['id']},
        })
        return nodes+edges
    if n4 > clicksrevne:
        clicksrevne = n4
        for i in G.edges:
            if i == (ltape['source'],ltape['target']):
                G.remove_edge(ltape['source'],ltape['target'])
        for i in edges:
            if i['data']['source'] == ltape['source'] and i['data']['target'] == ltape['target']:    
                edges.remove(i)
        return nodes+edges
    if n5 > clickschae:
        clickschae = n5
        for i in G.edges:
            if i == (ltape['source'],ltape['target']):
                G.remove_edge(ltape['source'],ltape['target'])
                G.add_weighted_edges_from([(ltape['source'],ltape['target'],int(value))])
        for i in edges:
            lk = i['data'].keys()
            for i in edges:
                if i['data']['source'] == ltape['source'] and i['data']['target'] == ltape['target']:    
                    edges.remove(i)
                    edges.append({'data': {'source': ltape['source'], 'target': ltape['target'], 'weight': value},})
            for i in edges:
                lk = i['data'].keys()
                if 'weight' not in lk:
                    auxxx = {'data': {'source': i['data']['source'], 'target': i['data']['target'], 'weight': '1',}}
                    edges.remove(i)
                    edges.append(auxxx)
        print(edges)
        return nodes+edges
    return m
@callback(Output('cytoscape-event-callbacks-1', 'stylesheet', allow_duplicate=True),
              Input('btn-ori-edge', 'n_clicks'),
              State('cytoscape-event-callbacks-1', 'stylesheet'),
              prevent_initial_call=True)
def changeori(n1,m):
    global ori,clicksori,style_edge,default_stylesheet,G
    if n1 > clicksori:
        clicksori = n1
        if ori:
            G.to_undirected()
            ori = False
            return default_stylesheet
        else:
            G.to_directed()
            ori = True
            return style_edge
    return m
@callback(Output('all', 'children'),
              Input('save', 'n_clicks'),
              Input('load', 'n_clicks'),
              State('input-on-submit-text-save', 'value'),
              State('bar', 'value'),
              State('cytoscape-event-callbacks-1', 'stylesheet'),
              State('all', 'children'))
def saveload(n1,n2,name,name2,m,og):
    global nodes,edges,G,lists,clickssav,clicksload
    file = open('saves.txt', 'r')
    saves = file.read()
    file.close()
    if n1>clickssav:
        clickssav = n1
        file = open(name+'GN.txt', 'w')
        file.write(str(G.nodes))
        file.close()
        file = open(name+'GE.txt', 'w')
        file.write(str(G.edges))
        file.close()
        file = open(name+'nodes.txt', 'w')
        file.write(str(nodes))
        file.close()
        file = open(name+'edges.txt', 'w')
        file.write(str(edges))
        file.close()
        if open('saves.txt','a'):
            if name not in saves:
                file = open('saves.txt', 'a')
                file.write(name+',')
                file.close()
        r = [
                dcc.Dropdown([saves.split(',')[i] for i in range(len(saves.split(','))) if saves.split(',')[i] != ''],str(name2),id = 'bar'),
                html.Br()
            ]
    if n2>clicksload:
      clicksload = n2
      if open(str(name2)+'GN.txt', 'r'): 
        file = open(str(name2)+'GN.txt', 'r')
        G.add_nodes_from(eval(file.read()))
        file.close()
        file = open(str(name2)+'GE.txt', 'r')
        G.add_edges_from(eval(file.read()))
        file.close()
        file = open(str(name2)+'nodes.txt', 'r')
        aux = file.read()
        nodes = eval(aux)
        file.close()
        file = open(str(name2)+'edges.txt', 'r')
        aux = file.read()
        edges = eval(aux)
        file.close()
        lists = saves
        r = [
                dcc.Dropdown([saves.split(',')[i] for i in range(len(saves.split(','))) if saves.split(',')[i] != ''],str(name2),id = 'bar'),
                html.Br()
            ]
    return og
@callback(Output('cytoscape-event-callbacks-1', 'elements', allow_duplicate=True),
              Input('upd', 'n_clicks'),
              State('cytoscape-event-callbacks-1', 'elements'),
              prevent_initial_call=True)
def update_g(_,__):
    global nodes,edges
    return nodes+edges
@callback(Output('result', 'children'),
        Output('cytoscape-event-callbacks-1', 'stylesheet'),
              Input('btn-bfs', 'n_clicks'),
              Input('btn-dfs', 'n_clicks'),
              State('cytoscape-event-callbacks-1', 'stylesheet'),
              prevent_initial_call=True)
def bfs(n1,n2,el):
    global ltap,clicksbfs,clicksdfs
    if n1 > clicksbfs:
        clicksbfs = n1
        o,d,pi,edc = bfs_aula(G,ltap['id'])
        print(edc)
        for i in edc:
            el.append({
                'selector': f'edge[source="{i[0]},target="{i[1]}"]',
                'style': {'line-color': 'red'}
            })
        print(el)
        r = "bfs D: "+str(d)+"\npi: "+str(pi)+"\no:"+str(o)
        return r, el
    if n2 > clicksdfs:
        clicksdfs = n2
        c,pi,d,f = dfs_aula(G)
        r = "dfs \n"
        for u in G.nodes():
            r = r+" "+str(u)+" "+str(c[u])+" "+str(pi[u])+" "+str(d[u])+" "+str(f[u])+"\n"
        return r,el
if __name__ == '__main__':
    print(type(nodes))
    app.run(debug=True)
