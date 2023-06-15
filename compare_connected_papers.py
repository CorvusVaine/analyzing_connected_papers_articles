#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import matplotlib
import networkx as nx
import igraph as ig
from igraph import Graph
import numpy as np

## Extract the bibliography from a file, here this file is generated for one article by Connected Papers and contains the references of he articles it is pointing to
def extract_bib (file):
    f = open(file,"r")
    lines = f.readlines()
    L_id = []
    L_titles = []
    for l in lines :
        if l[0]=="@":
            idd = l[9:-2]
            L_id.append(idd)
        if l[0:5]=="title":
            title = l[9:-3]
            L_titles.append(title)
    return(L_id,L_titles)

## Returns the articles in common between two bibliographies
def common_bib (file1,file2):
    bib1 = extract_bib(file1)
    bib2 = extract_bib(file2)
    bib_c_id = list(set(bib1[0]) & set(bib2[0]))
    bib_c_title = []
    for idd in bib_c_id:
        index_idd = bib1[0].index(idd)
        bib_c_title.append(bib1[1][index_idd])
    #bib_c_title = list(set(bib1[1]) & set(bib2[1]))
    return(bib_c_id,bib_c_title)

## Returns the number of appearances of each article in all bibliographies of files of a directory
def generate_nb_of_appearance_list(directory):
    bib = os.listdir(directory)
    bib = [bi for bi in bib if ".DS_Store" not in bi]
    bib = [bi for bi in bib if ".ipynb" not in bi]
    final = {}
    i=0
    for file in bib :
        file = directory+"/"+file
        bib_f = extract_bib(file)
        for i in range(len(bib_f[0])):
            if bib_f[0][i] in final:
                extr = final[bib_f[0][i]]
                extr[1]+=1
                final[bib_f[0][i]] = extr
            else :
                final[bib_f[0][i]]=[bib_f[1][i],1]
    return final

## Visualisation of this distribution 
def visualize_distrib(dico):
    values = dico.values()
    abs = [value[0] for value in values]
    ord = [value[1] for value in values]
    ord = [i for i in ord if i >2]
    print(ord)
    matplotlib.pyplot.hist(ord)
    return(abs,ord)

## Compute the edges from each article to the one it points to
def compute_edges(directory):
    L_edge = []
    bib = os.listdir(directory)
    bib = [bi for bi in bib if ".DS_Store" not in bi]
    bib = [bi for bi in bib if ".ipynb" not in bi]
    for file in bib :
        file = directory+"/"+file
        bib_f = extract_bib(file)
        L_id = bib_f[0]
        for v in L_id[1:]:
            L_edge.append((L_id[0],v))
    return(L_edge)

## Compute the weight of each link        
def compute_force_and_links(L_edges):
    D_force = {}
    D_links = {}
    for edge in L_edges:
        if edge[1] in D_force.keys():
            D_force[edge[1]]+=1
            D_links[edge[1]].append((edge[0],edge[1]))
        else :
            D_force[edge[1]]=1
            D_links[edge[1]]=[(edge[0],edge[1])]
    return D_force,D_links
    
## Filter the links by number of articles pointing TO an article (keeping only articles with at least deg articles pointing to them)
def filter_by_degree(D_links,deg):
    L_edges = []
    for v in D_links.keys():
        if len(D_links[v])>=deg:
            for l in D_links[v]:
                L_edges.append(l) 
    return L_edges

## Get the articles themselves
def vertices_from_edges(L_edges):
    L_vertices = list(set(list(sum(L_edges,()))))
    return L_vertices
#visualize_distrib(generate_nb_of_appearance_list("phenotype"))
        
# L_edges = compute_edges("binning")
# D_force,D_links = compute_force_and_links(L_edges)
# L_edges = filter_by_degree(D_links,4)
# L_vertices = vertices_from_edges(L_edges)
# print(L_edges)
# print(L_vertices)
# Gi = Graph(directed = True)
# Gi.add_vertices(L_vertices)
# Gi.add_edges(L_edges)
# layout = Gi.layout(layout='auto')
# ig.plot(Gi)
distr_all = visualize_distrib(generate_nb_of_appearance_list("all"))
distr_phen = visualize_distrib(generate_nb_of_appearance_list("phenotype"))
distr_bin = visualize_distrib(generate_nb_of_appearance_list("binning"))

X_axis = np.arange(1,24)
  
matplotlib.pyplot.bar(X_axis - 0.3, distr_all, 0.3, label = 'All')
matplotlib.pyplot.bar(X_axis + 0.3, distr_phen, 0.3, label = 'Phenotype')
matplotlib.pyplot.bar(X_axis, distr_bin, 0.3, label = 'Binning')

#print( [k for k in generate_nb_of_appearance_list("phenotype").values() if k[1]>3])