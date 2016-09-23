import os
import lstm
import lstm.generate

# run as single-threaded function
def run_single_run(seed, n_words=None, params=None, model="small", should_convert_to_unicode=True, max_per_seed=None):
    if params is None:
        if "DATAHACK_PARAMS" in os.environ:
            params = os.environ["DATAHACK_PARAMS"]
        else:
            params = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(lstm.__file__)), "..", "..", "params"))

    if max_per_seed is None:
        max_per_seed = int(os.environ.get("DATAHACK_MAXPERSEED", 50))

    if n_words is None:
        n_words = int(os.environ.get("DATAHACK_NUMWORDS", 60))

    FLAGS = lstm.generate.FLAGS
    FLAGS.seed = seed
    FLAGS.n_words = n_words
    FLAGS.checkpoint_dir = params
    FLAGS.model = model

    wordlist = lstm.generate.main(123.456, should_convert_to_unicode=should_convert_to_unicode)

    # TODO: smartify
    return list(set([
        x.strip()
        for x in " ".join(wordlist).split("\n")
        if len(x.split()) >= 3
    ]))[:max_per_seed]
