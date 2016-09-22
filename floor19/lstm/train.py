#! /usr/bin/env python
# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Example / benchmark for building a PTB LSTM model.

Trains the model described in:
(Zaremba, et. al.) Recurrent Neural Network Regularization
http://arxiv.org/abs/1409.2329

There are 3 supported model configurations:
===========================================
| config | epochs | train | valid  | test
===========================================
| small  | 13     | 37.99 | 121.39 | 115.91
| medium | 39     | 48.45 |  86.16 |  82.07
| large  | 55     | 37.87 |  82.62 |  78.29
The exact results may vary depending on the random initialization.

The hyperparameters used in the model:
- init_scale - the initial scale of the weights
- learning_rate - the initial value of the learning rate
- max_grad_norm - the maximum permissible norm of the gradient
- num_layers - the number of LSTM layers
- num_steps - the number of unrolled steps of LSTM
- hidden_size - the number of LSTM units
- max_epoch - the number of epochs trained with the initial learning rate
- max_max_epoch - the total number of epochs for training
- keep_prob - the probability of keeping weights in the dropout layer
- lr_decay - the decay of the learning rate for each epoch after "max_epoch"
- batch_size - the batch size

The data required for this example is in the data/ dir of the
PTB dataset from Tomas Mikolov's webpage:

$ wget http://www.fit.vutbr.cz/~imikolov/rnnlm/simple-examples.tgz
$ tar xvf simple-examples.tgz

To run:

$ python ptb_word_lm.py --data_path=simple-examples/data/

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

import numpy as np
import tensorflow as tf

from tensorflow.models.rnn.ptb import reader

from .model import PTBModel
from .config import get_config

flags = tf.flags
logging = tf.logging

flags.DEFINE_string(
    "model", "small",
    "A type of model. Possible options are: small, medium, large.")
flags.DEFINE_string("data_path", None, "data_path")
flags.DEFINE_bool("use_fp16", False,
                  "Train using 16-bit floats instead of 32bit floats")
flags.DEFINE_string("save_path", None, "Path for saving the trained parameters")

FLAGS = flags.FLAGS


def run_epoch(session, model, data, eval_op, verbose=False):
    """Runs the model on the given data."""
    epoch_size = ((len(data) // model.batch_size) - 1) // model.num_steps
    start_time = time.time()
    costs = 0.0
    iters = 0
    state = session.run(model.initial_state)
    for step, (x, y) in enumerate(reader.ptb_iterator(data, model.batch_size,
                                                      model.num_steps)):
        fetches = [model.cost, model.final_state, eval_op]
        feed_dict = {
            model.input_data: x,
            model.targets: y,
        }
        for i, (c, h) in enumerate(model.initial_state):
            feed_dict[c] = state[i].c
            feed_dict[h] = state[i].h
        cost, state, _ = session.run(fetches, feed_dict)
        costs += cost
        iters += model.num_steps

        if verbose and step % (epoch_size // 10) == 10:
            print("%.3f perplexity: %.3f speed: %.0f wps" %
                  (step * 1.0 / epoch_size, np.exp(costs / iters),
                   iters * model.batch_size / (time.time() - start_time)))

    return np.exp(costs / iters)


def main(_):
    if not FLAGS.data_path:
        raise ValueError("Must set --data_path to PTB data directory")

    raw_data = reader.ptb_raw_data(FLAGS.data_path)
    train_data, valid_data, test_data, _ = raw_data

    config = get_config(FLAGS.model)
    eval_config = get_config(FLAGS.model)
    eval_config.batch_size = 1
    eval_config.num_steps = 1

    with tf.Graph().as_default(), tf.Session() as session:
        initializer = tf.random_uniform_initializer(-config.init_scale,
                                                    config.init_scale)
        with tf.variable_scope("model", reuse=None, initializer=initializer):
            m = PTBModel(is_training=True, config=config, use_fp16=FLAGS.use_fp16)
        with tf.variable_scope("model", reuse=True, initializer=initializer):
            mvalid = PTBModel(is_training=False, config=config, use_fp16=FLAGS.use_fp16)
            mtest = PTBModel(is_training=False, config=eval_config, use_fp16=FLAGS.use_fp16)
            saver = tf.train.Saver()

        tf.initialize_all_variables().run()

        for i in range(config.max_max_epoch):
            lr_decay = config.lr_decay ** max(i - config.max_epoch, 0.0)
            m.assign_lr(session, config.learning_rate * lr_decay)

            print("Epoch: %d Learning rate: %.3f" % (i + 1, session.run(m.lr)))
            train_perplexity = run_epoch(session, m, train_data, m.train_op,
                                         verbose=True)
            print("Epoch: %d Train Perplexity: %.3f" % (i + 1, train_perplexity))
            valid_perplexity = run_epoch(session, mvalid, valid_data, tf.no_op())
            print("Epoch: %d Valid Perplexity: %.3f" % (i + 1, valid_perplexity))

        test_perplexity = run_epoch(session, mtest, test_data, tf.no_op())
        print("Test Perplexity: %.3f" % test_perplexity)

        if FLAGS.save_path is not None:
            saver.save(session, FLAGS.save_path + '/model.ckpt')

if __name__ == "__main__":
    tf.app.run()
