import pandas as pd
import networkx as nx
import json

df = pd.read_csv('https://raw.githubusercontent.com/umassdgithub/Week-8-part-1/main/data/data_scopus.csv')

G = nx.Graph()

# Node Creation
for idx, row in df.iterrows():
    if isinstance(row['Authors with affiliations'], float) or row['Authors with affiliations'] == "":
        continue

    authors = row['Authors with affiliations'].split(';')
    citations = len(authors);

    first_author = row['Authors'].split(',')[0].strip()
    country = authors[0].split(',')[-1].strip()

    G.add_node(row['Title'], country=country, fauthor=first_author,no_of_citations=citations) #Node with properties

# Loop all rows while comparing with all the data
for idx1, row1 in df.iterrows():
    for idx2, row2 in df.iterrows():
        if idx1 != idx2:
            first_author = authors[0].split(',')[0].strip()
            authors1 = set(row1['Authors'].split(','))
            authors2 = set(row2['Authors'].split(','))
            if len(authors1.intersection(authors2)) > 0:
                G.add_edge(row1['Title'], row2['Title'])

# Extract by country
nodes_by_country = {}
for node in G.nodes:
    if 'country' not in G.nodes[node]:
        continue
    country = G.nodes[node]['country']
    if country not in nodes_by_country:
        nodes_by_country[country] = []
    nodes_by_country[country].append(node)

# Rearrange data by country
graphs_by_country = {}
for country, nodes in nodes_by_country.items():
    graphs_by_country[country] = G.subgraph(nodes).copy()

data = {'nodes': [], 'links': []}
for country, graph in graphs_by_country.items():
    for node in graph.nodes:
        if 'country' not in graph.nodes[node]:
            continue
        data['nodes'].append({'id': node, 'country': graph.nodes[node]['country'], 'fauthor': graph.nodes[node]['fauthor'], 'citations': graph.nodes[node]['no_of_citations']})
    for edge in graph.edges:
        data['links'].append({'source': edge[0], 'target': edge[1]})

with open('data.json', 'w') as f:
    json.dump(data, f)
