from collections import Counter
import numpy as np
import nltk
from nltk.stem.lancaster import LancasterStemmer
from HebrewTokenizer import *
import json
ENGLISH_STOPWORDS = []
HEBREW_STOPWORDS = []
TFIDF_FILENAME = '../data/ynet_all_types_500_articles_tf_idf.txt'

class TextProcessing(object):
    def __init__(self, text):
        self.text = text
        self.st = LancasterStemmer()
        for line in open(TFIDF_FILENAME, 'r'):
            self.idf_dict = json.loads(line)

    def getFreqDict(self, hebrew=True):
        if hebrew:
            cleaned_words_list = self.cleanTextHebrew(self.text)
        else:
            cleaned_words_list = self.cleanTextEnglish(self.text)
        print "cleaned_words_list", cleaned_words_list
        sum_words = len(cleaned_words_list)
        freq_dict = dict((word, count/float(sum_words)) for word, count in Counter(cleaned_words_list).iteritems())
        tfidf = {}
        for d in freq_dict.items():
            print d[0], "in idf:", self.idf_dict.get(d[0].decode('UTF-8'),0)
            tfidf[d[0]] = self.idf_dict.get(d[0],0)*d[1]
        return tfidf

    def cleanTextEnglish(self, text):
        all_kw = []
        for w in nltk.word_tokenize(text):
            ww = self.st.stem(w).lower()
            if ww.isalpha and ww not in ENGLISH_STOPWORDS:
                all_kw.append(ww)
        #### TODO - change all_kw to be a a list of all KW in space
        return self.removeWordNotInSpace(all_kw, all_kw)

    def cleanTextHebrew(self, text):
        tok_s = []
        for i in tokenize(text):
            if i[0] == "HEB":
                tok_s.append(i[1])
        return tok_s

   
    def removeWordNotInSpace(self, word_sen, gen_space):
        return np.intersect1d(word_sen, gen_space)


