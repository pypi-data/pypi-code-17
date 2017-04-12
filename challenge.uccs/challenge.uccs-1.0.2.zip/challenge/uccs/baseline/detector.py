import bob.core
logger = bob.core.log.setup("challenge.UCCS")

import bob.io.base
import bob.io.image
import bob.ip.color
import bob.ip.facedetect
import numpy
import math
import os
import multiprocessing

from .. import utils

def command_line_options(command_line_arguments):
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--data-directory', '-d', required=True, help = "Select the directory, where the UCCS image files are stored")
  parser.add_argument('--result-file', '-w', default = os.path.join("results", "UCCS-detection-baseline.txt"), help = "Select the file to write the scores into")
  parser.add_argument('--which-set', '-y', default = "validation", choices = ("training", "validation", "test", "sample"), help = "Select the protocol to use")

  parser.add_argument('--maximum-detections', '-M', type=int, default=20, help = "Specify, how many detections per image should be stored")
  parser.add_argument('--number-of-overlaps', '-o', type=int, default=5, help = "If given, only detections with the given number of overlapping detections are considered")
  parser.add_argument('--absolute-threshold', '-t', type=float, default=10, help = "If given, only detections with predictions above this threshold will be used.")
  parser.add_argument('--relative-threshold', '-T', type=float, default=0.5, help = "Limits detections to those that have a prediction value higher than --relative-threshold * max(predictions)")

  parser.add_argument('--cascade-file', '-r', help = "The file to read the resulting cascade from; If left empty, the default cascade will be loaded")
  parser.add_argument('--distance', '-s', type=int, default=2, help = "The distance with which the image should be scanned.")
  parser.add_argument('--scale-factor', '-S', type=float, default = math.pow(2.,-1./16.), help = "The logarithmic distance between two scales (should be between 0 and 1).")
  parser.add_argument('--lowest-scale', '-f', type=float, default = 0.0625, help = "Faces which will be lower than the given scale times the image resolution will not be found.")
  parser.add_argument('--detection-overlap', '-b', type=float, default=0.25, help = "If given, the average of the overlapping detections with this minimum overlap will be considered.")

  parser.add_argument('--parallel', '-P', type=int, help = "If given, images will be processed with the given number of parallel processes")

  parser.add_argument('--display', '-x', action='store_true', help = "Displays preprocessed images (waits for user keypress); not in parallel mode")
  parser.add_argument('--debug', '-q', type=int, help = "Use only a subset of the data")


  bob.core.log.add_command_line_option(parser)
  args = parser.parse_args(command_line_arguments)
  bob.core.log.set_verbosity_level(logger, args.verbose)

  if args.parallel is not None and args.display:
    logger.warn("Disabling --display (-x) as we run in parallel mode")
    args.display = False

  return args

def _align(b,q):
  # turns the BoundingBox C++ object into a (picklable) list so that it can be returned through multiprocessing
  return b.left_f, b.top_f, b.size_f[1], b.size_f[0], q

def _parallel(arguments):
  # get process ID
  p = multiprocessing.current_process().name
  process_id = int(p.split('-')[1]) if p != 'MainProcess' else -1

  image_files, args, gt_bounding_boxes = arguments
  # load classifier and feature extractor; each process needs its own cascade
  if args.cascade_file is None:
    if abs(process_id) == 1:
      logger.info("Using default frontal face detection cascade from bob.ip.facedetect")
    cascade = bob.ip.facedetect.default_cascade()
  else:
    if abs(process_id) == 1:
      logger.info("Loading cascade from file '%s'", args.cascade_file)
    cascade = bob.ip.facedetect.detector.Cascade(bob.io.base.HDF5File(args.cascade_file))
  # initialize sampler
  sampler = bob.ip.facedetect.detector.Sampler(patch_size=cascade.extractor.patch_size, distance=args.distance, scale_factor=args.scale_factor, lowest_scale=args.lowest_scale)

  logger.debug("Processing %d images%s", len(image_files), (" in process %d" % process_id) if process_id > 0 else "")
  detections = {}
  for image_file in image_files:
    try:
      # load image
      image = bob.io.base.load(os.path.join(args.data_directory, args.which_set, image_file))

      # get bounding boxes and their qualities
      faces = bob.ip.facedetect.detect_all_faces(image, cascade, sampler, args.absolute_threshold, args.number_of_overlaps, args.detection_overlap, args.relative_threshold)

      if faces is not None:
        # there are detected faces
        bounding_boxes, qualities = faces

        # sort bbxs and qualities by qualities descendingly
        bounding_boxes, qualities = (list(x) for x in zip(*sorted(zip(bounding_boxes, qualities), key=lambda pair: pair[1], reverse=True)))
      else:
        # no detected faces
        bounding_boxes, qualities = [], []

      # sort bbxs and qualities by qualities descendingly
      bounding_boxes, qualities = (list(x) for x in zip(*sorted(zip(bounding_boxes, qualities), key=lambda pair: pair[1], reverse=True)))

      # save best detections
      detections[image_file] = [_align(bounding_boxes[i], qualities[i]) for i in range(min(args.maximum_detections, len(qualities)))]

      if not detections[image_file]:
        logger.warn("No face was found for image %s", image_file)
      else:
        logger.debug("Detected %d faces in image %s", len(detections[image_file]), image_file)

      if args.display:
        # for displaying purposes only
        from matplotlib import pyplot, patches
        pyplot.figure("Detections")
        pyplot.clf()
        pyplot.imshow(numpy.transpose(image, (1,2,0)))

        # show detections
        if detections[image_file]:
          min_quality = args.absolute_threshold
          quality_range = max(max(bbx[4] for bbx in detections[image_file]) - min_quality, 1e-4)

          for bbx in detections[image_file]:
            pyplot.gca().add_patch(patches.Rectangle(bbx[:2], bbx[2], bbx[3], fill=False, color='g', lw=4.*(bbx[4] - min_quality)/quality_range + 1))

        # show ground truth
        if gt_bounding_boxes is not None:
          for _,bbx in gt_bounding_boxes[image_file]:
            if bbx is not None:
              pyplot.gca().add_patch(patches.Rectangle(bbx[:2], bbx[2], bbx[3], fill=False, color='r', lw=3, ls=':'))

        raw_input("Detections in image %s; Press Enter to continue" % image_file)
    except Exception as e:
      logger.error("File %s: error %s", image_file, e)

  logger.debug("Finished processing%s" % (" process %d" % process_id) if process_id > 0 else "")
  return detections


def main(command_line_arguments = None):

  # get command line arguments
  args = command_line_options(command_line_arguments)

  # load protocol
  logger.info("Loading UCCS %s protocol", args.which_set)
  data = utils.read_ground_truth(args.data_directory, args.which_set)
  image_names = sorted(data.keys())

  if args.debug:
    # limit the data to the given number of images (debug mode only)
    image_names = image_names[:args.debug]

  if args.parallel is None:
    logger.info("Detecting faces in %d images", len(image_names))
    # no parallelization; process all images sequentially; the ground truth "dataT is used for display purposes only
    detections = _parallel((image_names, args, data))
  else:
    # parallelization; split data into chunks
    logger.info("Detecting faces in %d images using %d parallel processes", len(image_names), args.parallel)
    detections = {}
    pool = multiprocessing.Pool(args.parallel)
    splits = utils.split_data_list_into_parallel(image_names, args.parallel, (args, None))
    # process each chunk in a different process
    for d in pool.imap_unordered(_parallel, splits):
      detections.update(d)

  logger.info("Writing result file to %s", args.result_file)
  bob.io.base.create_directories_safe(os.path.dirname(args.result_file))
  with open(args.result_file, "w") as f:
    if command_line_arguments is None:
      import sys
      command_line_arguments = sys.argv
    f.write("# Created using command line: %s\n" % " ".join(command_line_arguments))
    f.write("# FILE,BB_X,BB_Y,BB_WIDTH,BB_HEIGHT,DETECTION_SCORE\n")
    for image in sorted(detections.keys()):
      for bbx in detections[image]:
        f.write("%s,%3.2f,%3.2f,%3.2f,%3.2f,%3.2f\n" % (image, bbx[0], bbx[1], bbx[2], bbx[3], bbx[4]))
