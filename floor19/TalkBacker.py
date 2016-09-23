# coding: utf-8
#!/usr/bin/env python

import nltk
from TextSimilarity import TextSimilarity
import json
TFIDF_FILENAME = '../data/ynet_all_types_500_articles_tf_idf.txt'
from HebrewTokenizer import *

nltk.download('punkt')

# GIVEN_ARTICLE = 'the best country in the world is Israel'
# GIVEN_HEADER_FILE = 'Israel'
# OPTIONAL_TALKBACKS = ["country forever", "a country", "b"]

# GIVEN_ARTICLE = "היום יום שני לחודש, זהו יום מאוד יפה".decode("UTF-8")
# GIVEN_HEADER_FILE = "יום".decode("UTF-8")
OPTIONAL_TALKBACKS = map(lambda s:s.decode("UTF-8"), ["התרגיל מחירי מוצרים", "מעניין אם...", "שווה להיות סלב!", "התמונות יום", "ספורט זבל..."])

GIVEN_ARTICLE = None
GIVEN_HEADER_FILE = None

def cleanTextHebrew(text):
    tok_s = []
    for i in tokenize(text):
            if i[0] == "HEB":
                tok_s.append(i[1])
    return tok_s
    
class TalkBacker(object):

    def __init__(self, given_article=GIVEN_ARTICLE, header_text=GIVEN_HEADER_FILE):
        print "given_article", given_article
        print "header_text", header_text
        self.given_article = given_article
        self.header_text = header_text
        for line in open(TFIDF_FILENAME, 'r'):
            self.idf_dict = json.loads(line)

    def suggest(self):
        optional_talkbacks = self.getAllOptinalTalkBacks()
        print "given_article", self.given_article
        print "optional_talkbacks", optional_talkbacks

        best_talkback_score = 0
        best_talkback = None
        for talkback in optional_talkbacks:
            print "----------------"
            current_score = TextSimilarity(self.given_article, talkback).calcSimilarity()
            if current_score > best_talkback_score:
                best_talkback_score = current_score
                best_talkback = talkback
            print "----------------"

        return best_talkback, best_talkback_score

    def getArticleTopWords(self, header_text):
        return header_text[0]

    def getAllOptinalTalkBacks(self):
        seed = self.getSeeds(self.header_text)
        return self.getModelResult(seed)

    def getModelResult(self, seed):
        return OPTIONAL_TALKBACKS

    def getSeeds(self, header_text):
        title_kw = cleanTextHebrew(header_text)
        title_kw_score = {}
        for t in title_kw:
            title_kw_score[t] = self.idf_dict.get(t,0)
        return sorted(title_kw_score.items(), key=lambda x: x[1])[::-1][:10]
        #return header_text[0]

if __name__ == "__main__":
    TalkBacker().suggest()
