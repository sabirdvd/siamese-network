'''
Iterator utilities for Siamese Network Training

1. Labeled Dataset iterator
'''

import os
from collections import namedtuple

import tensorflow as tf
from tensorflow.contrib import data

#Setup TF logging
logging = tf.logging
logging.set_verbosity(logging.INFO)

'''
Convert a textline dataset to an array of word indexes and length of array

Inputs
* dataset_file_path: Each line contains one string
* vocab_table: Vocab lookup table initialized using lookup_ops
'''
def create_wordindex_with_length_dataset(dataset_file_path, vocab_table):
  text_dataset = data.TextLineDataset(dataset_file_path)
  text_dataset = text_dataset.map(lambda line: tf.string_split([line]).values)
  text_dataset = text_dataset.map(lambda words: vocab_table.lookup(words))
  text_dataset = text_dataset.map(lambda words: (tf.cast(words, tf.int32), tf.size(words)))
  return text_dataset


class BatchedInput(namedtuple('BatchedInput', 'txt1 txt2 len_txt1 len_txt2 label init')):
  pass


def create_labeled_data_iterator(txt1, txt2, labels, vocab_table, batch_size):
  text1_dataset = create_wordindex_with_length_dataset(txt1, vocab_table)
  text2_dataset = create_wordindex_with_length_dataset(txt2, vocab_table)

  # Labels is a single float
  labels_dataset = data.TextLineDataset(labels)
  labels_dataset = labels_dataset.map(lambda line: tf.string_to_number(line))
  labels_dataset = labels_dataset.map(lambda label: tf.cast(label, tf.float32))

  dataset = data.Dataset.zip((text1_dataset, text2_dataset, labels_dataset))

  # Separate out lengths of txt1 and txt2
  dataset = dataset.map(lambda t1, t2, label: (t1[0], t2[0], t1[1], t2[1], label))

  # Create a padded batch
  dataset = dataset.padded_batch(batch_size, padded_shapes=(
  tf.TensorShape([None]), tf.TensorShape([None]), tf.TensorShape([]), tf.TensorShape([]), tf.TensorShape([])))

  iterator = dataset.make_initializable_iterator()
  txt1, txt2, len_txt1, len_txt2, label = iterator.get_next()

  return BatchedInput(txt1, txt2, len_txt1, len_txt2, label, iterator.initializer)