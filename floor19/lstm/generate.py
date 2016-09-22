#! /usr/bin/env python

import tensorflow as tf

from .model import PTBModel
from .config import get_config

flags = tf.flags

flags.DEFINE_string(
    "model", "small",
    "A type of model. Possible options are: small, medium, large.")
flags.DEFINE_bool("use_fp16", False,
                  "Train using 16-bit floats instead of 32bit floats")
flags.DEFINE_string("checkpoint_file", None, "file with saved model parameters")
flags.DEFINE_integer('n_words', 1, "number of words")

FLAGS = flags.FLAGS


def main(_):
    if FLAGS.checkpoint_file is None:
        raise ValueError("Must set --checkpoint_file")

    eval_config = get_config(FLAGS.model)
    eval_config.batch_size = 1
    eval_config.num_steps = 1

    with tf.Graph().as_default(), tf.Session() as session:
        initializer = tf.random_uniform_initializer(-eval_config.init_scale,
                                                    eval_config.init_scale)

        with tf.variable_scope("model", reuse=None, initializer=initializer):
            model = PTBModel(is_training=False, config=eval_config, use_fp16=FLAGS.use_fp16)
            saver = tf.train.Saver()

        tf.initialize_all_variables().run()

        saver.restore(session, FLAGS.checkpoint_file)
        print "Model parameters restored from disk"

        # for i in range(config.max_max_epoch):
        #     lr_decay = config.lr_decay ** max(i - config.max_epoch, 0.0)
        #     m.assign_lr(session, config.learning_rate * lr_decay)
        #
        #     print("Epoch: %d Learning rate: %.3f" % (i + 1, session.run(m.lr)))
        #     train_perplexity = run_epoch(session, m, train_data, m.train_op,
        #                                  verbose=True)
        #     print("Epoch: %d Train Perplexity: %.3f" % (i + 1, train_perplexity))
        #     valid_perplexity = run_epoch(session, mvalid, valid_data, tf.no_op())
        #     print("Epoch: %d Valid Perplexity: %.3f" % (i + 1, valid_perplexity))
        #
        # test_perplexity = run_epoch(session, mtest, test_data, tf.no_op())
        # print("Test Perplexity: %.3f" % test_perplexity)
        #
        # if FLAGS.save_path is not None:
        #     saver.save(session, FLAGS.save_path + '/model.ckpt')


if __name__ == "__main__":
    tf.app.run()
