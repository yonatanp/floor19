import nltk
from TextSimilarity import TextSimilarity

# TODO: to be replaced
GIVEN_ARTICLE = 'abc'
OPTIONAL_TALKBACKS = ['a', 'r', 't']

nltk.download('punkt')

class TalkBacker(object):

    def __init__(self, given_article):
        self.given_article = given_article

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

    def getArticleTopWords(self, text):
        # TODO: in the meanwhile - all article
        return text

    def getAllOptinalTalkBacks(self):
        return OPTIONAL_TALKBACKS

#if __name__ == "__main__":
# from floor19.TalkBacker import TalkBacker
# given_article = 'abc'
# TalkBacker(given_article).suggest()
