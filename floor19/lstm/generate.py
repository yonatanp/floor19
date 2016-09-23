#! /usr/bin/env python

import os
import pickle
import numpy as np
import tensorflow as tf

from .model import PTBModel
from .config import get_config

flags = tf.flags

flags.DEFINE_string(
    "model", "small",
    "A type of model. Possible options are: small, medium, large.")
flags.DEFINE_bool("use_fp16", False,
                  "Train using 16-bit floats instead of 32bit floats")
flags.DEFINE_string("checkpoint_dir", None, "folder with saved model parameters")
flags.DEFINE_string('seed', None, "initial word")
flags.DEFINE_integer('n_words', 1, "number of words to generate")

FLAGS = flags.FLAGS


def generate(session, model, seed, n_words, eval_op, unknown=None):
    words = [seed]

    state = session.run(model.initial_state)

    for n in xrange(n_words):
        fetches = [model.cost, model.final_state, model.probabilities, model.logits, eval_op]

        x = np.array([words[-1:]])

        feed_dict = {
            model.input_data: x,
            model.targets: x,
        }

        for i, (c, h) in enumerate(model.initial_state):
            feed_dict[c] = state[i].c
            feed_dict[h] = state[i].h

        cost, state, probs, logits, _ = session.run(fetches, feed_dict)

        s = sorted(xrange(probs.shape[1]), key=lambda _x: probs[0, _x], reverse=True)
        words.append(s[s[0] == unknown])
        # words.append(np.argmax(probs, 1)[0])

    return words


def main(_, should_convert_to_unicode=False):
    if FLAGS.checkpoint_dir is None:
        raise ValueError("Must set --checkpoint_dir")

    if FLAGS.seed is None:
        raise ValueError("Must set --seed")

    with open(os.path.join(FLAGS.checkpoint_dir, "vocabulary.pkl")) as f:
        utf_vocab = pickle.load(f)

    if should_convert_to_unicode:
        vocab = dict((x.decode("utf-8"),y) for (x,y) in utf_vocab.iteritems())
    else:
        vocab = utf_vocab

    backvocab = {y: x for x, y in vocab.iteritems()}
    if should_convert_to_unicode:
        backvocab[vocab[u'unknown']] = '---'
        backvocab[vocab[u'<eos>']] = '\n'
    else:
        backvocab[vocab['unknown']] = '---'
        backvocab[vocab['<eos>']] = '\n'

    print "--- vocab: %d items, e.g. %s" % (len(vocab), vocab.keys()[:5])


    if FLAGS.seed not in vocab:
        raise ValueError("Seed '%s' not in vocabulary" % (FLAGS.seed,))

    config = get_config(FLAGS.model)
    config.vocab_size = len(vocab)
    config.batch_size = 1
    config.num_steps = 1

    with tf.Graph().as_default(), tf.Session() as session:
        initializer = tf.random_uniform_initializer(-config.init_scale, config.init_scale)

        with tf.variable_scope("model", reuse=None, initializer=initializer):
            model = PTBModel(is_training=False, config=config, use_fp16=FLAGS.use_fp16)
            saver = tf.train.Saver()

        tf.initialize_all_variables().run()

        ckpt = tf.train.get_checkpoint_state(FLAGS.checkpoint_dir)

        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(session, ckpt.model_checkpoint_path)
            # print "Model parameters restored from disk"

        else:
            print "No checkpoint found!"
            return

        words = generate(session, model, vocab[FLAGS.seed], FLAGS.n_words, tf.no_op(), unknown=vocab['unknown'])

        result = [backvocab[x] for x in words]
        print ' '.join(result)
        # for x in words:
        #     print backvocab[x]

        return result

if __name__ == "__main__":
    tf.app.run()
