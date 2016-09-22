import numpy as np
import collections
from TextProcessing import TextProcessing

class TextSimilarity(object):

    def __init__(self, text1, text2):
        self.text1 = text1
        self.text2 = text2

    def calcSimilarity(self):
        freq_dict1 = self.getFreqDict(self.text1)
        freq_dict2 = self.getFreqDict(self.text2)
        print "freq_dict1", freq_dict1
        print "freq_dict2", freq_dict2
        # fill missing keys
        self._fillMissingKeys(freq_dict1, freq_dict2)
        # calc cosine distance (note we assume the same order of values)
        freq_dict1_od = collections.OrderedDict(sorted(freq_dict1.items()))
        freq_dict2_od = collections.OrderedDict(sorted(freq_dict2.items()))
        return self._calcCosineDistance(freq_dict1_od.values(), freq_dict2_od.values())

    def getFreqDict(self, text):
        return TextProcessing(text).getFreqDict()

    def _fillMissingKeys(self, freq_dict1, freq_dict2):
        all_keys = freq_dict1.keys() + freq_dict2.keys()
        for k in all_keys:
            if k not in freq_dict1:
                freq_dict1[k] = 0
            if k not in freq_dict2:
                freq_dict2[k] = 0
        print "_fillMissingKeys: freq_dict1", freq_dict1
        print "_fillMissingKeys: freq_dict2", freq_dict2


    def _calcCosineDistance(self, a, b):
        print "_calcCosineDistance: a,b", a,b
        # use numpy's dot product to calculate the cosine similarity
        cosine_score = np.dot(a, b) / np.sqrt(np.dot(a, a) * np.dot(b, b))
        print "cosine_score", cosine_score
        return cosine_score