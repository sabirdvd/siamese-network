import logging, argparse
import numpy as np

R1 = 0
R2 = 1
R5 = 4

def setup_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-scores_file')
  parser.add_argument('-map_file')
  parser.add_argument('-k', type=int, default=10)
  parser.add_argument('-num_datum', default=19560, type=int)
  args = parser.parse_args()
  return args


def find_rank_index(index, candidates):
  for rank, candidate in enumerate(candidates):
    if candidate[1] == index:
      return rank


def process_candidates(candidates, max_rank, datum_num):
  #Sorry, no candidates!
  if len(candidates) == 0:
    return

  #GT is not present in candidates, set rank_gt=k
  if candidates[0][1] != 0:
    return

  candidates = sorted(candidates, key=lambda candidate: candidate[0], reverse=True)
  rank_0 = find_rank_index(0, candidates)
  max_rank[datum_num] = rank_0

def main():
  args = setup_args()
  logging.info(args)

  #We want to compute Rank of index=0 (GT)
  #By default this is set to Max_Candidates+1
  rank_gt = [args.k for datum in range(args.num_datum)]
  mrr = [0.0 for _ in range(args.num_datum)]

  #These two are used to compute compression we can obtain
  total_datums = 0.0
  total_candidates = 0.0

  last_datum_num = 0
  candidates = []

  #Map contains two numbers datum and index of candidate in original file..
  for scores_line, map_line in zip(open(args.scores_file), open(args.map_file)):
    datum_num, index = map_line.split(',')
    datum_num = int(datum_num)

    #Datum index changed, we can thus now process all candidates gathered so far
    if datum_num != last_datum_num:
      total_candidates += len(candidates)
      total_datums += 1

      process_candidates(candidates, rank_gt, last_datum_num)
      if rank_gt[last_datum_num] == args.k:
        logging.info('Datum: %d GT absent C: %d'%(last_datum_num, len(candidates)))
      else:
        mrr[last_datum_num] = 1.0 / (rank_gt[last_datum_num] + 1)
        logging.info('Datum: %d Rank_0: %d/%d'%(last_datum_num, rank_gt[last_datum_num], len(candidates)-1))
      last_datum_num = datum_num
      candidates = []

    index = int(index)
    score = float(scores_line.strip())
    candidates.append((score, index))

  #This for the last set
  process_candidates(candidates, rank_gt, last_datum_num)
  logging.info('Datum: %d Rank_0: %d/%d' % (last_datum_num, rank_gt[last_datum_num], len(candidates)-1))

  num_r1 = 0.0
  num_r2 = 0.0
  num_r5 = 0.0

  gt_present = 0
  gt_absent = 0
  total = 0.0 + len(rank_gt)
  #Given Rank of GT for each datum, it is trivial to compute R@k numbers
  for datum in rank_gt:
    if datum == args.k:
      gt_absent += 1
    else:
      gt_present += 1

    if datum == R1:
      num_r1 += 1
      num_r2 += 1
      num_r5 += 1
    elif datum <= R2:
      num_r2 += 1
      num_r5 += 1
    elif datum <= R5:
      num_r5 += 1

  logging.info('R1:%d R2:%d R@5:%d GT(%d/%d)' % (int(num_r1), int(num_r2), int(num_r5), gt_present, gt_absent))
  logging.info('R@1:%.4f R@2:%.4f R@5:%.4f Avg:%.4f MRR: %.4f'%((num_r1/total), (num_r2/total), (num_r5/total),
                                                      (total_candidates/total_datums), np.average(mrr)))

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
  main()