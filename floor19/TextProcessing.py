from collections import Counter
import numpy as np
import nltk
from nltk.stem.lancaster import LancasterStemmer
from HebrewTokenizer import *

ENGLISH_STOPWORDS = ["at", "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
HEBREW_STOPWORDS = []

class TextProcessing(object):
    def __init__(self, text):
        self.text = text
        self.st = LancasterStemmer()

    def getFreqDict(self, hebrew=True):
        if hebrew:
            cleaned_words_list = self.cleanTextHebrew(self.text)
        else:
            cleaned_words_list = self.cleanTextEnglish(self.text)
        print "cleaned_words_list", cleaned_words_list
        sum_words = len(cleaned_words_list)
        freq_dict = dict((word, count/float(sum_words)) for word, count in Counter(cleaned_words_list).iteritems())
        return freq_dict

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


