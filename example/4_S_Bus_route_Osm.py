#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This example shows an example in which we will read a geoJson file with the 
help of geopandas and extract useful information and visualize with the help
of Kepler.

@author: ikespand
"""
import os
from settings import *
from keplergl_cli.keplergl_cli import Visualize
import geopandas as gpd
from shapely.ops import nearest_points
from geopy.distance import geodesic
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

"""
# %% Geopandas can parse geojson
fname = "busStops.geojson"
gdf = gpd.read_file(fname)

#%%
gdf['id'] = gdf['id'].map(lambda x: x.lstrip('node/')).astype("int")
gdf = gdf.drop(columns=["@id","name:kn"])
gdf["osmid"] = gdf['id']
#gdf = gdf.set_index('id')


def getXY(pt):
    return (pt.x, pt.y)

centroidseries = gdf['geometry'].centroid
x,y = [list(t) for t in zip(*map(getXY, centroidseries))]

gdf["y"] = y
gdf["x"] = x

aa = gdf.head(500)
#aa.crs = {'init' :'epsg:4326'}

G = nx.Graph()

for j in range(0, len(aa)):
    G.add_node(aa["osmid"][j], pos=(aa["x"][j], aa["y"][j]))

for col in aa.columns:
    nx.set_node_attributes(G, name=col, values=aa[col].dropna())

nx.draw(G, nx.get_node_attributes(G, 'pos'), node_size=5)
#aa.to_file("output.json", driver="GeoJSON")
from shapely.geometry import Point

pt = Point(77.59,12.99)
np1 =[o.wkt for o in nearest_points(pt, aa.geometry.unary_union)][1]

pt = Point(77.29,13.01)
np2 =[o.wkt for o in nearest_points(pt, aa.geometry.unary_union)][1]

print(nx.shortest_path(G, source=np1, target=np2))
"""
#%%
fname = "routes.geojson"
gdf1 = gpd.read_file(fname)

#av_node = gdf1.tail(213)

rel = gdf1.head(13)
rel = rel.reset_index(drop=True)

rel1 = rel[rel["id"]=="relation/5598563"]

rel2 = rel[rel["id"]=="relation/9740040"]

rel3 = rel[rel["id"]=="relation/9385446"]

#rel1.to_file("output.json", driver="GeoJSON")

def get_node_df(rel_singlerow_gdf):
    x=[]
    y=[]
    for point in rel_singlerow_gdf.geometry.iloc[0].coords:
        x.append(point[0])
        y.append(point[1])
        
    
    data = pd.DataFrame()  
    data["x"] = x
    data["y"] = y
    data["node"] = data.index
    
    return data

def build_edges_from_nodes(data):
    a= []
    b= []
    c =[]
    for k in range(0, (len(data)-1)):
        a.append(data["node"][k])
        b.append(data["node"][k+1])
        distance = geodesic((data["x"][k],data["y"][k]), (data["x"][k+1],data["y"][k+1])).meters #geopy distance
        c.append(distance)
    
    data_ls  = pd.DataFrame()  
    data_ls["node1"] = a
    data_ls["node2"] = b
    data_ls["distance"] = c
    
    return data_ls

nodes_data_1 = get_node_df(rel1)
nodes_data_2 = get_node_df(rel2)
nodes_data_3 = get_node_df(rel3)

nodes_data_2["node"] = nodes_data_2["node"] + 1000
nodes_data_3["node"] = nodes_data_3["node"] + 2000
#%%
# Find the duplicates nodes 
s1 = pd.merge(nodes_data_1, nodes_data_2, how='inner', on=['x','y'])
s1 = pd.merge(s1, nodes_data_3, how='inner', on=['x','y'])

#%%
for k in range(0, len(s1)):
    nodes_data_2["node"][nodes_data_2["node"]==s1["node_y"][k]] = s1["node_x"][k]
    nodes_data_3["node"][nodes_data_3["node"]==s1["node"][k]] = s1["node_x"][k]


    
edge_data_1 = build_edges_from_nodes(nodes_data_1)
edge_data_2 = build_edges_from_nodes(nodes_data_2)
edge_data_3 = build_edges_from_nodes(nodes_data_3)

#%%

nodes_merge = pd.concat([nodes_data_1, nodes_data_2, nodes_data_3])
edges_merge = pd.concat([edge_data_1, edge_data_2, edge_data_3])
nodes_merge = nodes_merge.reset_index(drop=True)
edges_merge = edges_merge.reset_index(drop=True)


G = nx.Graph()    
#G = nx.from_pandas_dataframe(data_ls, 'node1', 'node2', ['distance'])
G = nx.from_pandas_edgelist(edges_merge, 'node1', 'node2',['distance'])
for m in range(0, len(nodes_merge)):
    G.add_node(nodes_merge["node"][m], pos=(nodes_merge["x"][m], nodes_merge["y"][m]))

path =nx.shortest_path(G, source=30, target=2151, weight = 'distance')

print(path)

pos = nx.get_node_attributes(G, 'pos')
nx.draw(G,pos,node_color='k',node_size=1)
# draw path in red
path = nx.shortest_path(G,source=0,target=2001)
path_edges = zip(path,path[1:])
path_edges = set(path_edges)
nx.draw_networkx_nodes(G,pos,nodelist=path,node_color='r',node_size=1)
nx.draw_networkx_edges(G,pos,edgelist=path_edges,edge_color='r',width=1)
plt.axis('equal')
plt.show()    






















#---------
#from networkx.readwrite import json_graph
#import json
#
#data1 =json_graph.node_link_data(G)
#
#with open('data.json', 'w') as f:
#    json.dump(data1, f)
# %% Visualize with Kepler
vis = Visualize(api_key=MAPBOX_API_KEY,
                config_file="keplergl_config.json",
                output_map="S_Bus_route_Osm")
# Add the data to Visualize
vis.add_data(data=geodf, names='Bus Route')
# Save the output map and do not open it
html_path = vis.render(open_browser=False,
                       read_only=False)

#%%
import osmnx as ox

places = ['Los Altos, California, USA',
          {'city':'Los Altos Hills', 'state':'California'},
          'Loyola, California']
G = ox.graph_from_place(places, network_type='drive')
ox.plot_graph(G)