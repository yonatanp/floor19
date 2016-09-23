# coding: utf-8
#!/usr/bin/env python

import nltk
from TextSimilarity import TextSimilarity

nltk.download('punkt')

# GIVEN_ARTICLE = 'the best country in the world is Israel'
# GIVEN_HEADER_FILE = 'Israel'
# OPTIONAL_TALKBACKS = ["country forever", "a country", "b"]

# GIVEN_ARTICLE = "היום יום שני לחודש, זהו יום מאוד יפה".decode("UTF-8")
# GIVEN_HEADER_FILE = "יום".decode("UTF-8")
OPTIONAL_TALKBACKS = map(lambda s:s.decode("UTF-8"), ["קרב תרבות בטקס", "מעניין אם...", "שווה להיות סלב!", "התמונות יום", "ספורט זבל..."])

GIVEN_ARTICLE = None
GIVEN_HEADER_FILE = None

class TalkBacker(object):

    def __init__(self, given_article=GIVEN_ARTICLE, header_text=GIVEN_HEADER_FILE):
        print "given_article", given_article
        print "header_text", header_text
        self.given_article = given_article
        self.header_text = header_text

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
        #getArticleTopWords
        return OPTIONAL_TALKBACKS

if __name__ == "__main__":
    TalkBacker().suggest()
