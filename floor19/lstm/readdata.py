from tensorflow.models.rnn.ptb.reader import _build_vocab, _file_to_word_ids


def load_data(filename):
    word_mapping = _build_vocab(filename)
    data = _file_to_word_ids(filename, word_mapping)
    return data, word_mapping
