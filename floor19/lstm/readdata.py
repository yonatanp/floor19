import tensorflow as tf
from collections import Counter


def read_words(filename):
    with tf.gfile.GFile(filename, "r") as f:
        return f.read().replace("\n", " <eos> ").split()


def build_vocab(filename):
    data = read_words(filename)

    counter = Counter(data)
    count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))

    words, _ = list(zip(*count_pairs))
    word_to_id = dict(zip(words, range(len(words))))

    return word_to_id


def file_to_word_ids(filename, word_to_id):
    data = read_words(filename)
    return [word_to_id[word] for word in data]


def load_data(filename):
    vocabulary = build_vocab(filename)
    data = file_to_word_ids(filename, vocabulary)
    return data, vocabulary
