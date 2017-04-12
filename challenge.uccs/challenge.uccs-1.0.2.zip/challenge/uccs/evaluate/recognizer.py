#!/mgunther/test_checkouts/bob.bio.caffe/bin/python

import bob.core
logger = bob.core.log.setup("challenge.UCCS")

import numpy
import math
import os
from .. import utils

import bob.measure

from bob.ip.facedetect import BoundingBox

def command_line_options(command_line_arguments):
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--data-directory', '-d', required=True, help = "Select the directory, where the UCCS data files are stored")
  parser.add_argument('--result-files', '-r', nargs='+', required=True, help = "Get the file with the face recognition results")
  parser.add_argument('--overlap-threshold', '-t', type=float, default=0.5, help = "The overlap threshold for detected faces to be considered to be detected correctly")
  parser.add_argument('--rank', '-R', type=int, default=1, help = "Plot DIR curves for the given rank")
  parser.add_argument('--labels', '-l', nargs='+', help = "Use these labels; if not given, the filenames will be used")
  parser.add_argument('--dir-file', '-w', default = "DIR.pdf", help = "The file, where the DIR curve will be plotted into")
  parser.add_argument('--only-present', '-x', action="store_true", help = "Only caluclate the results for files that have been detected (for debug purposes only)")
  parser.add_argument('--log-x', '-s', action='store_true', help = "If selected, plots will be in semilogx")

  bob.core.log.add_command_line_option(parser)
  args = parser.parse_args(command_line_arguments)
  bob.core.log.set_verbosity_level(logger, args.verbose)

  if args.labels is None:
    args.labels = args.result_files

  return args


def split(subject, bbx, scores):
  # splits the detections for this image into positives and negatives
  # takes the scores for the bbx with the highest overlap with the GT
  gt = utils.bounding_box(bbx)
  overlaps = sorted([(utils.overlap(gt, utils.bounding_box(d)), s) for d, s in scores], reverse=True, key=lambda x: x[0])

  if overlaps[0][0] == 0:
    # no overlap -> no positives and no negatives
    return [], []
  best_scores = overlaps[0][1]

  positives = [best_scores[subject]] if subject in best_scores else []
  negatives = [best_scores[s] for s in best_scores if s != subject]

  return negatives, positives

def split_by_probe(ground_truth, scores, args):
  scores_by_probe = {}
  for image in ground_truth:
    if image not in scores and args.only_present:
      continue

    for subject, bbx in ground_truth[image]:
      key = (image, subject)
      if key not in scores_by_probe:
        scores_by_probe[key] = (subject, [], [])
      _, negatives, positives = scores_by_probe[key]
      if image in scores:
        neg, pos = split(subject, bbx, scores[image])
        # we ignore all positives for subject -1
        # TODO: implement better strategy?
        if subject != -1 and pos:
          positives.extend(pos)
        # we always add the negatives, if present
        if neg:
          if subject == -1:
            # for unknowns, we only use the maximum score
            # i.e., we consider only the top match score as a negative (see handbook of face recognition)
            negatives.append(max(neg))
          else:
            # else, we use all of them
            negatives.extend(neg)

  return scores_by_probe


def get_misdetections(ground_truth, scores, args):
  # computes all scores that are assigned to bounding boxes of the background
  # and that are not assigned as -1
  background_negatives = []
  for image in scores:
    assert image in ground_truth
    # check all bounding boxes
    for bbx, labels in scores[image]:
      det = utils.bounding_box(bbx)
      if all(utils.overlap(det, utils.bounding_box(d)) < args.overlap_threshold for _,d in ground_truth[image]):
        # no overlap to ground-truth bounding boxes; all negatives
        negatives = [score for subject,score in labels.items() if subject != -1]
        if negatives:
          # consider only the top match score as a negative
          background_negatives.append(max(negatives))

  logger.info("Collected %d labeled background regions in %d images", len(background_negatives), len(scores))
  return background_negatives

def detection_identification_rate(scores_by_probe, misdetections, args):
  # collect all negatives, i.e., scores for which the identity is not in the gallery -- subject id -1
  negatives = sorted(max(neg) for subject,neg,_ in scores_by_probe.values() if subject == -1 if len(neg))
  # add all misdetections (background region labeled other than -1) as negatives
  negatives.extend(misdetections)

  assert negatives, "At least one negative without positive is required"
  logger.info("Counted a total of %d scores for unknown faces", len(negatives))

  # compute FAR values
  if args.log_x:
    # get false alarms in a log scale
    base = math.pow(10., 1./8.)
    false_alarm_counts = [math.pow(base,i) for i in range(int(math.log(len(negatives), base)))] + [len(negatives)]
  else:
    false_alarm_counts = range(0,len(negatives),50) + [len(negatives)]
  fa_values = [float(c) / len(negatives) for c in false_alarm_counts]

  # and compute thresholds
  thresholds = [bob.measure.far_threshold(negatives, [], v, True) for v in fa_values]

  # now, get the DIR for the given thresholds
  counter = 0.
  correct = numpy.zeros(len(thresholds))
  for subject, neg, pos in scores_by_probe.values():
    # for the DIR, we only count identities that are in the gallery
    if subject != -1:
      counter += 1.

      # compute the rank of the positive, if any
      if pos:
        if len(pos) != 1:
          logger.warning("We have %d positive scores %s for subject %d; taking the first one", len(pos), pos, subject)
        pos = pos[0]
        if not neg:
          neg = []
        is_detected = sum(n >= pos for n in neg) < args.rank
        if is_detected:
          for i,t in enumerate(thresholds):
            # ... increase the number of correct detections, when the positive is over threshold
            if pos >= t:
              correct[i] += 1

  # normalize by the counters
  correct *= 100./counter

  return false_alarm_counts, correct


def main(command_line_arguments = None):

  # get command line arguments
  args = command_line_options(command_line_arguments)
  # read the detections
  # read the ground truth bounding boxes of the validation set
  logger.info("Reading UCCS ground-truth")
  ground_truth = utils.read_ground_truth(args.data_directory, "validation")

  results = []
  max_fa = 0
  for result_file in args.result_files:
    logger.info("Reading scores from %s", result_file)
    scores = utils.read_recognitions(result_file)

    logger.info("Computing Rates")
    scores_by_probe = split_by_probe(ground_truth, scores, args)
    logger.info("Evaluating %d faces of known identities", len(scores_by_probe)-1)
    misdetections = get_misdetections(ground_truth, scores, args)
    fa, dir_ = detection_identification_rate(scores_by_probe, misdetections, args)

    results.append((fa, dir_))
    max_fa = max(max_fa, fa[-1])

  logger.info("Plotting DIR curve(s) to file '%s'", args.dir_file)
  # import matplotlib and set some defaults
  from matplotlib import pyplot
  pyplot.ioff()
  import matplotlib
  matplotlib.rc('text', usetex=True)
  matplotlib.rc('font', family='serif')
  matplotlib.rc('lines', linewidth = 4)
  # increase the default font size
  matplotlib.rc('font', size=18)

  # now, plot
  figure = pyplot.figure()
  plotter = pyplot.semilogx if args.log_x else pyplot.plot
  for i, label in enumerate(args.labels):
    # compute some thresholds
    plotter(results[i][0], results[i][1], label=label)

  # finalize plot
  if args.log_x:
    pyplot.xticks((1, 10, 100, 1000), ["1", "10", "100", "1000"])
    pyplot.xlim([1,max_fa])
  else:
    pyplot.xlim([0,max_fa])

  pyplot.grid(True, color=(0.6,0.6,0.6))
  pyplot.title("Rank %d DIR curve" % args.rank)
  pyplot.legend(loc=1,prop={'size': 16})
  pyplot.xlabel('Number of False Alarms')
  pyplot.ylim((0, 100))
  pyplot.ylabel('Detection \& Identification Rate in \%%')
  pyplot.tight_layout()
  pyplot.savefig(args.dir_file)
