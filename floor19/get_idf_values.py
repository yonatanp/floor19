
# coding: utf-8

import numpy as np
import json
from HebrewTokenizer import *
from TextProcessing import *

def cleanTextHebrew(text):
    tok_s = []
    for i in tokenize(text):
        if i[0] == "HEB":
            tok_s.append(i[1])
    return tok_s

def calc_idf(docs):
    token_docs = []
    counts_kw = {}
    idf_vals = {}
    N = float(len(docs))
    for d in docs:
        tok_doc = cleanTextHebrew(d)
        token_docs.append(tok_doc)
    all_voc_list = np.unique([item for sublist in token_docs for item in sublist])
    print "I AM HERE"
    for token_d in token_docs:
        join_kw = np.intersect1d(token_d, all_voc_list) # unique values
        for kw in join_kw:
            counts_kw[kw] = counts_kw.get(kw, 0) + 1
    for k in counts_kw.items():
        idf_vals[k[0]] = np.log10(float(N)/k[1])
    return idf_vals

def calc_idf_for_file(data_type="articles", type_f="a"):
    f = "../data/ynet_national_500_%s.json" % data_type
    articles = []
    for line in open(f, 'r'):
        articles.append(json.loads(line))
    if data_type=="articles":
        articles_text = [i['full_text'] for i in articles]
    else:
        articles_text = [i['title_text'] for i in articles]
    idf_articles = calc_idf(articles_text)
    idf_art = sorted(idf_articles.items(), key=lambda x: x[1])
    # write all KWs, after tokenizing. 
    with open("../data/ynet_national_500_%s_idf_vals.txt" % data_type, 'w') as outfile:
        json.dump(idf_articles, outfile)
    return idf_art


def _get_raw_data(datatype = "articles"):  #"talkbacks"
    data = []
    for t in ["cars", "dating","digital","economy","education","health","national","parents","politics"]:
        f = "../data/ynet_%s_500_%s.json" % (t, datatype)
        for line in open(f, 'r'):
            data.append(json.loads(line))
    return data



#articles_text = [i['full_text'] for i in articles]
#idf_articles = calc_idf(articles_text)
