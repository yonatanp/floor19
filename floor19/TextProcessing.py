from collections import Counter
import numpy as np
import nltk
from nltk.stem.lancaster import LancasterStemmer
from HebrewTokenizer import *
import json

ENGLISH_STOPWORDS = []
HEBREW_STOPWORDS = []
TFIDF_FILENAME = '../data/ynet_all_types_500_articles_tf_idf.txt'
HEBREW = True

class TextProcessing(object):
    def __init__(self, text):
        self.text = text
        self.st = LancasterStemmer()
        with open(TFIDF_FILENAME, 'r') as f:
            self.idf_dict = json.load(f)

    def getFreqDict(self, hebrew=HEBREW, exclude_punct=True):
        if hebrew:
            cleaned_words_list = self.cleanTextHebrew(exclude_punct)
        else:
            cleaned_words_list = self.cleanTextEnglish(exclude_punct)
        #print "cleaned_words_list", cleaned_words_list
        sum_words = len(cleaned_words_list)
        freq_dict = dict((word, count/float(sum_words)) for word, count in Counter(cleaned_words_list).iteritems())
        tfidf = {}
        for d in freq_dict.items():
            #print d[0], "in idf:", self.idf_dict.get(d[0].decode('UTF-8'),0)
            try:
                tfidf[d[0]] = self.idf_dict.get(d[0], 0)*d[1]
            except Exception:
                print "failed!!!!"
                import traceback
                print repr(d[0])
                traceback.print_exc()
                raise
                continue
        return tfidf

    def cleanTextEnglish(self, exclude_punct=True):
        all_kw = []
        for w in nltk.word_tokenize(self.text):
            ww = self.st.stem(w).lower()
            if ww.isalpha and ww not in ENGLISH_STOPWORDS:
                all_kw.append(ww)
        #### TODO - change all_kw to be a a list of all KW in space
        return self.removeWordNotInSpace(all_kw, all_kw)

    def cleanTextHebrew(self, exclude_punct=True):
        tok_s = []
        for i in tokenize(self.text):
            if exclude_punct:
                if i[0] == "HEB":
                    tok_s.append(i[1])
            else:
                tok_s.append(i[1])
        return tok_s

    def removeWordNotInSpace(self, word_sen, gen_space):
        return np.intersect1d(word_sen, gen_space)


