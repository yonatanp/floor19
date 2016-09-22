import numpy as np

class TextSimilarity(object):

    def calcSimilarity(self, freq_dict1, freq_dict2):
        # fill missing keys
        self._fillMissingKeys(freq_dict1, freq_dict2)
        # calc cosine distance (note we assume the same order of values)
        return self._calcCosineDistance(freq_dict1.values(), freq_dict2.values())

    def _fillMissingKeys(self, freq_dict1, freq_dict2):
        all_keys = freq_dict1.keys() + freq_dict2.keys()
        for k in all_keys:
            if k not in freq_dict1:
                freq_dict1[k] = 0
            if k not in freq_dict2:
                freq_dict2[k] = 0

    def _calcCosineDistance(self, a, b):
        # use numpy's dot product to calculate the cosine similarity
        return np.dot(a, b) / np.sqrt(np.dot(a, a) * np.dot(b, b))