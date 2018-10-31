'''
Visualizes and analyzes social networks
Takes input data from socilab for LinkedIn networks
Takes input data from Lost Circles for Facebook networks
'''

import tkinter as tk
from tkinter import filedialog
import json, csv
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import operator

def new_network():
    g = nx.Graph()
    return g

def build_facebook_net():
    fbg = new_network()

    #Have user pick the Facebook network JSON data file
    root = tk.Tk()
    root.withdraw()
    file_path = tk.filedialog.askopenfilename()

    #Read data as dict and drop unnecessary elements
    with open(file_path) as json_data:
        data = json.load(json_data)
    data.pop('userName')
    data.pop('userId')

    fromList = []
    toList = []

    #Add connections between your friends
    for i in data['links']:
        fromList.append(i['source'])
        toList.append(i['target'])
        
    #Add connections between you and your friends
    for i in range(0, len(data['nodes'])):
        fromList.append(0)  #Let 0 be your node Id
        toList.append(i+1)
        
    #Populate nodes for everyone in your network plus yourself
    for i in range(0, len(data['nodes'])+1):
        fbg.add_node(i, label=i)
        
    #Populate edges for all connections in your network
    for i in range(0, len(fromList)):
        fbg.add_edge(fromList[i], toList[i], key=i)

    return fbg

def build_linkedin_net():
    #Have user pick the LinkedIn network csv data file
    root = tk.Tk()
    root.withdraw()
    file_path = tk.filedialog.askopenfilename()
    
    #Read the csv file as a data frame
    data = pd.read_csv(file_path, index_col=0)
    
    #Build the network
    lg = nx.from_numpy_matrix(data.values)
    return lg

'''
linkedin_net = build_linkedin_net()
#Plot LinkedIn network
nx.draw(linkedin_net)
plt.show()
'''

facebook_net = build_facebook_net()

#Degree centrality top 10
deg = nx.degree(facebook_net)
deg=dict(deg)
deg_sorted = sorted(deg.items(), key=operator.itemgetter(1), reverse=True)
print("Top 10 degree centrality (node, centrality): ", deg_sorted[0:9])
#Closeness centrality top 10
clo = nx.closeness_centrality(facebook_net)
clo_sorted = sorted(clo.items(), key=operator.itemgetter(1), reverse=True)
print("Top 10 closeness centrality (node, centrality): ", clo_sorted[0:9])
#Betweenness centrality top 10
bet = nx.betweenness_centrality(facebook_net)
bet_sorted = sorted(bet.items(), key=operator.itemgetter(1), reverse=True)
print("Top 10 betweenness centrality (node, centrality): ", bet_sorted[0:9])
#Eigenvector centrality top 10
eig = nx.eigenvector_centrality(facebook_net)
eig_sorted = sorted(eig.items(), key=operator.itemgetter(1), reverse=True)
print("Top 10 eigenvector centrality (node, centrality): ", eig_sorted[0:9])
#Pagerank centrality top 10
pag = nx.pagerank(facebook_net)
pag_sorted = sorted(pag.items(), key=operator.itemgetter(1), reverse=True)
print("Top 10 pagerank centrality (node, centrality): ", pag_sorted[0:9])

#Trim network to only show nodes with more than 1 connection
facebook_net_trimmed = facebook_net.copy()
for n in facebook_net_trimmed.nodes():
    if deg[n] < 2:
        facebook_net_trimmed.remove_node(n)

#View all cliques
cliques = list(nx.find_cliques(facebook_net_trimmed))
print("Cliques:")
for c in cliques:
    print(c)

#Export data for use in Gephi
nx.write_gexf(facebook_net, "facebook_network.gexf")

#Plot Facebook network
nx.draw_random(facebook_net)
plt.show()


