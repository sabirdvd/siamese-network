from model import SiameseModel
import tensorflow as tf
import argparse
import codecs, json

from tensorflow.python.ops import lookup_ops
from tensorflow.contrib.learn import ModeKeys
from iterator_utils import create_data_iterator

logging = tf.logging
logging.set_verbosity(logging.INFO)


def setup_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-hparams_file')
  parser.add_argument('-model_dir')
  parser.add_argument('-txt1')
  parser.add_argument('-txt2')
  parser.add_argument('-out')

  args = parser.parse_args()
  return args

def load_hparams(hparams_file):
  if tf.gfile.Exists(hparams_file):
    logging.info("# Loading hparams from %s" % hparams_file)
    with codecs.getreader("utf-8")(tf.gfile.GFile(hparams_file, "rb")) as f:
      try:
        hparams_values = json.load(f)
        hparams = tf.contrib.training.HParams(**hparams_values)
      except ValueError:
        logging.info("  can't load hparams file")
        return None
    return hparams
  else:
    return None


def main():
  args = setup_args()
  logging.info(args)

  #Load Hparams
  hparams = load_hparams(args.hparams_file)
  logging.info(hparams)

  vocab_table = lookup_ops.index_table_from_file(hparams.vocab_path, default_value=0)
  iterator = create_data_iterator(args.txt1, args.txt2, vocab_table, 16)
  infer_model = SiameseModel(hparams, iterator, ModeKeys.INFER)

  with tf.Session() as sess:
    sess.run(tf.tables_initializer())
    latest_ckpt = tf.train.latest_checkpoint(args.model_dir)
    infer_model.saver.restore(sess, latest_ckpt)

    infer_model.compute_scores(sess, args.out)

if __name__ == '__main__':
  main()