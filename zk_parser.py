import markdown
import pandas as pd
from os import listdir
from os.path import isfile, join
import networkx as nx

from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.palettes import Blues8, Reds8, Purples8, Oranges8, Viridis8, Spectral8
from bokeh.transform import linear_cmap
from networkx.algorithms import community


mypath = '..'
filelist = [f for f in listdir(mypath) if isfile(join(mypath, f))]
filelist = [f for f in filelist if '.md' in f]
cols = ['id', 'title', 'author' , 'tags' ,'links']
zk = pd.DataFrame(columns=cols)

for f in filelist:
    with open("../"+f, "r", encoding="utf-8") as input_file:
        text = input_file.read()


    title = text.split('#title ')[1].split('\n')[0]
    author = text.split('#author ')[1].split('\n')[0]
    file_id = text.split('ID: ')[1].split('\n')[0].split(' ')[-1]
    heads = [text.split('#')[i].split('\n')[0] for i in range(len(text.split('#')))]
    tags = []; reserved = ['literature ', 'reference', ' Metadata', '', ' ']
    for t in heads:
        if t.split(' ')[0] not in reserved:
            if title not in t and author not in t:
                tags.append(t.split(' ')[0])

    links = [text.split('[[')[i].split(']]')[0] for i in range(1, len(text.split('[[')))]

    row = [file_id, title, author, tags, links]
    zk.loc[len(zk)] = row


#todo - parse HTML result from zotero bibliography and match citations based on title to dataframe
#pyzotero docs: https://pyzotero.readthedocs.io/en/latest/
# zk.to_csv('zk_012121.csv')
# from pyzotero import zotero
# zotero_user = 7404811
# zotero_key = 'CfBLE4xzHEMo8bMsufYVR8ql'
# zot = zotero.Zotero(zotero_user, 'user', zotero_key)
# zot.add_parameters(format='bib')
# bibliography = zot.items()


#jupyter notebook for visualization: https://nbviewer.jupyter.org/github/jkbren/presilience/blob/master/code/01_Intro_Network_Resilience.ipynb

#get set of all possible tags as nodes
tag_nodes = []
for i in range(len(zk)):
    for j in range(len(zk.iloc[i].tags)):
        t = zk.iloc[i].tags[j]
        if t not in tag_nodes:
            tag_nodes.append(t)

#get list of literature nodes
lit_nodes = zk.id.tolist()

#make list of total nodes
nodes = tag_nodes + lit_nodes

#create edges from tags
edges = []
for i in range(len(zk)):
    lit = zk.iloc[i]
    for j in range(len(lit.tags)):
        tag = zk.iloc[i].tags[j]
        edges.append((lit.id, tag))

#create edges from links
for i in range(len(zk)):
    lit = zk.iloc[i]
    for j in range(len(lit.links)):
        link = zk.iloc[i].links[j]
        edges.append((lit.id, link))

#create graph
G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

#calculate node degrees
degrees = dict(nx.degree(G))
nx.set_node_attributes(G, name='degree', values=degrees)

#plot graph
title = 'Zettelkasten'

#Establish which categories will appear when hovering over each node
HOVER_TOOLTIPS = [("ID", "@index"), ("Degree", "@degree")]

#Create a plot — set dimensions, toolbar, and title
plot = figure(tooltips = HOVER_TOOLTIPS,
              tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
            x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)

#Create a network graph object with spring layout
network_graph = from_networkx(G, nx.spring_layout, scale=500, center=(0, 0))

#Set node size and color
network_graph.node_renderer.glyph = Circle(size=15, fill_color='skyblue')

#Set edge opacity and width
network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)

#Add network graph to the plot
plot.renderers.append(network_graph)

show(plot)

#Color if tag or non-tag
#selective highlighting
#Size based on degree
#https://melaniewalsh.github.io/Intro-Cultural-Analytics/Network-Analysis/Making-Network-Viz-with-Bokeh.html

