#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyzotero import zotero
import pandas
import matplotlib.pyplot as plt

## Returns a dictionary linking each article of a collection to a list of all its tags
def extract_tags(coll):
    dict_tags ={}
    for item in coll :
        L_tags = []
        D_tags = item['data']['tags']
        for tag in D_tags :
            L_tags.append(tag["tag"])
        dict_tags[item["data"]["title"]] = L_tags
    return(dict_tags)

## Returns the list of all tags used in the dataset of articles 
def get_tags_list(dico) :
    tag_list = []
    for k in dico.keys():
        val = dico[k]
        for tag in val :
            if tag not in tag_list: 
                tag_list.append(tag)
    return(sorted(tag_list))

## Returns a dataframe returning a matrix of presence of tags for ech article
def boolean_tags(dico,list_tags):
    bool_dico = {}
    for article in dico.keys() :
        one_hot_tags = []
        for tag in list_tags :
            if tag in dico[article]:
                one_hot_tags.append(True)
            else :
                one_hot_tags.append(False)
        bool_dico[article] = one_hot_tags
    return(pandas.DataFrame.from_dict(bool_dico,orient = "index",columns = list_tags))

## Returns the cardinal of each tag
def effect_tags(df):
    return(df.sum(axis = 0))

## The tags were grouped in my dataset. This function allows to get the cardinal of each group. It i only relevant in my dataset, for it is hardcoded, but it can be adapted.
def eff_by_groups(eff_tags,option):
    if option == "all":
        return(eff_tags)
    if option == "B":
        return(eff_tags[0:6])
    if option == "E":
        return(eff_tags[6:14])
    if option == "F":
        return(eff_tags[14:32])
    if option == "M":
        return(eff_tags[32:43])
    
## Returns a dictionnary linking each article of a collection to its abstract
def extract_abstract(coll):
    D_abs = {}
    for item in coll :
        title = item['data']['title']
        abstract = item['data']['abstractNote']
        D_abs[title]=abstract
    return D_abs

## Returns True if elem (often an abstract) contains at least one metagenomic keyword and one deep learning keyword.
def filter_by_equation(elem):
    Bool_meta = False
    Bool_deep = False
    Bool_none = False
    meta_words = ["Metagenomics","metagenomics","METAGENOMICS","Metagenomic","metagenomic","METAGENOMIC","Metagenome","metagenome","METAGENOME","Microbiome","microbiome","MICROBIOME"]
    deep_words = ["interpretable","long short-term memory" ,"deep learning" ,"nlp" ,"transformer","cnn","convolutional","lstm","neural network" ,"bert","natural language processing","autoencoder","Interpretable","Long Short-Term Memory" ,"Long short-term memory" ,"long Short-term memory" ,"long short-Term memory" ,"long short-term Memory" ,"Long Short-term memory" ,"Long short-Term memory" ,"Long short-term Memory" ,"long Short-Term memory" ,"long Short-term Memory" ,"long short-Term Memory" ,"Long Short-Term memory" ,"Long Short-term Memory" ,"Long short-Term Memory" ,"long Short-Term Memory" ,"Deep Learning" ,"Deep learning","deep Learning","Nlp" ,"Transformer","Cnn","Convolutional","Lstm","Neural Network","neural Network","Neural network" ,"Bert","Natural Language Processing","Natural language processing","natural Language processing","natural language Processing","Natural Language processing","natural Language Processing","Natural language Processing","Autoencoder","INTERPRETABLE","LONG SHORT-TERM MEMORY" ,"DEEP LEARNING" ,"NLP" ,"TRANSFORMER","CNN","CONVOLUTIONAL","LSTM","NEURAL NETWORK" ,"BERT","NATURAL LANGUAGE PROCESSING","AUTOENCODER","embedding","Embedding","EMBEDDING"]
    if elem == '':
        Bool_none = True
    if Bool_none == True :
        return "Check"
    else :
        for m in meta_words:
            if m in elem :
                Bool_meta=True
        for d in deep_words:
            if d in elem :
                Bool_deep=True
        return(Bool_meta and Bool_deep)
 
## Takes the return of extract_abstract as a parameter and returns a list of each article with a booleans corresponding to the presence of one keyword from each list
def presence_dico(dico):
    dico_ans = {}
    for title in dico.keys():
        abst = dico[title]
        dico_ans[title]=filter_by_equation(abst)
    return dico_ans

## Tahes a dictionary of articles and returns a dictionary of the articles not bearing this tag
def articles_without_tag(items,tag):
    dic_tag = {}
    for arti in items.keys():
        if tag not in items[arti]:
            dic_tag[arti]=items[arti]
    return(dic_tag)
    
## Tahes a dictionary of articles and returns a dictionary of the articles bearing this tag
def articles_with_tag(items,tag):
    dic_tag = {}
    for arti in items.keys():
        if tag in items[arti]:
            dic_tag[arti]=items[arti]
    return(dic_tag)

library_id = your_library_id
library_type = 'group'
api_key = your_api_key
zot = zotero.Zotero(library_id, library_type, api_key)
coll = zotero.Zotero.collections(zot)
items = zot.top()
dico_tags = extract_tags(items)
tags_list = get_tags_list(dico_tags)
bool_df = boolean_tags(dico_tags,tags_list)
eff_tags = effectif_tags(bool_df)
eff_tags = eff_by_groups(eff_tags,"all")
