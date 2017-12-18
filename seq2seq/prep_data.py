import argparse, logging

EOU = '__eou__'
EOT = '__eot__'


def setup_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-stopw', help='stopwords file')
  parser.add_argument('-word_clusters', help='Word clusters')
  parser.add_argument('-txt1')
  parser.add_argument('-txt2')
  parser.add_argument('-labels', default=None)
  parser.add_argument('-out_txt1')
  parser.add_argument('-out_txt2')
  parser.add_argument('-out_index')
  args = parser.parse_args()
  return args


def build_cluster_map(file_name):
  with open(file_name) as fr:
    clusters = []
    word2cluster = {}

    for line in fr:
      cluster = line.split()
      for word in cluster:
        assert word not in word2cluster
        word2cluster[word] = len(clusters)
      clusters.append(cluster)
  return word2cluster, clusters


def read_stopwords(file_name):
  stop_words = set()
  with open(file_name) as fr:
    for line in fr:
      stop_words.add(line.strip())
  return stop_words


def get_cluster_repr(sentence, word2cluster, clusters):
  cluster_ints = [word2cluster[word] for word in sentence.split() if word in word2cluster]
  sorted_clusters = sorted(list(set(cluster_ints)))
  cluster_words = [clusters[cluster][0] for cluster in sorted_clusters]
  return cluster_words


def process_target(sentence, word2cluster, clusters):
  cluster_words = get_cluster_repr(sentence, word2cluster, clusters)
  return cluster_words


def process_source(sentence, word2cluster, clusters):
  final_words = []
  for turn in sentence.split(EOT)[:-1]:
    for utt in turn.split(EOU)[:-1]:
      words = [clusters[word2cluster[word]][0] if word in word2cluster else word for word in utt.split()]
      final_words.extend(words)
      final_words.append(EOU)
    final_words.append(EOT)
  return final_words


def main():
  args = setup_args()
  logging.info(args)

  stopw = read_stopwords(args.stopw)
  logging.info('#Stopwords: %d'%len(stopw))

  word2cluster, clusters = build_cluster_map(args.word_clusters)
  logging.info('#Clusters: %d Word assigned:%d'%(len(clusters), len(word2cluster)))

  fw_txt1 = open(args.out_txt1, 'w')
  fw_txt2 = open(args.out_txt2, 'w')
  fw_index = open(args.out_index, 'w')

  index = 0
  for txt1, txt2, label in zip(open(args.txt1), open(args.txt2), open(args.labels)):
    label = int(label)
    if label == 0:
      index += 1
      continue

    txt2_clusters = process_target(txt2, word2cluster, clusters)
    if len(txt2_clusters) == 0:
      index += 1
      continue

    txt1_words = process_source(txt1, word2cluster, clusters)
    fw_txt1.write('%s\n'%' '.join(txt1_words))
    fw_txt2.write('%s\n'%' '.join(txt2_clusters))
    fw_index.write('%d\n'%index)
    index += 1


if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
  main()