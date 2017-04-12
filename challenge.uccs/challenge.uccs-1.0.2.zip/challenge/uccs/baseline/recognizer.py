#!/mgunther/bob/bob-stable/py27/bin/python

import sys
import os

import bob.core
logger = bob.core.log.setup("challenge.UCCS")

import bob.io.base
import bob.io.image
import bob.ip.base
import bob.ip.color
import bob.ip.facedetect
import bob.learn.linear
import numpy
import scipy.spatial

import math
import bob.io.base
import multiprocessing

from .. import utils

def command_line_options(command_line_arguments):
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--data-directory', '-d', required=True, help = "Select the directory, where image files are stored")
  parser.add_argument('--result-file', '-w', default = "results/UCCS-recognition-baseline.txt", help = "Select the file to write the scores into")
  parser.add_argument('--detector-result-file', '-i', help = "If given, use the detection result file")
  parser.add_argument('--no-train-on-unknowns', '-u', action='store_true', help = "If selected, the known unknowns will not be used as a separate class")
  parser.add_argument('--no-redetect-training-images', '-n', action='store_true', help = "If selected, training set bounding boxes will not be re-detected")
  parser.add_argument('--eigenvalue-energy', '-e', type = float, default = .99, help = "Select the PCA energy that is kept")
  parser.add_argument('--maximum-scores', '-m', type=int, default=10, help = "Specify, how many scores per validation image should be stored")

  parser.add_argument('--maximum-detections', '-M', type=int, default=20, help = "Specify, how many detections per image should be stored")
  parser.add_argument('--number-of-overlaps', '-o', type=int, default=5, help = "If given, only detections with the given number of overlapping detections are considered")
  parser.add_argument('--absolute-threshold', '-t', type=float, default=10, help = "If given, only detections with predictions above this threshold will be used.")
  parser.add_argument('--relative-threshold', '-T', type=float, default=0.5, help = "Limits detections to those that have a prediction value higher than --relative-threshold * max(predictions)")

  parser.add_argument('--cascade-file', '-r', help = "The file to read the resulting cascade from; If left empty, the default cascade will be loaded")
  parser.add_argument('--distance', '-s', type=int, default=2, help = "The distance with which the image should be scanned.")
  parser.add_argument('--scale-factor', '-S', type=float, default = math.pow(2.,-1./16.), help = "The logarithmic distance between two scales (should be between 0 and 1).")
  parser.add_argument('--lowest-scale', '-f', type=float, default = 0.0625, help = "Faces which will be lower than the given scale times the image resolution will not be found.")
  parser.add_argument('--detection-overlap', '-b', type=float, default=0.25, help = "If given, the average of the overlapping detections with this minimum overlap will be considered.")

  parser.add_argument('--training-image-file', default='temp/UCCS-Detected-Training-Images.hdf5', help = "Set intermediate file, where re-detected training bounding boxes are stored")

  parser.add_argument('--projector-file', default='temp/UCCS-Projector.hdf5', help = "Set intermediate file, where Projector is stored")
  parser.add_argument('--models-file', default='temp/UCCS-Models.hdf5', help = "Set intermediate file, where the models are stored")
  parser.add_argument('--probes-file', default='temp/UCCS-Probes.hdf5', help = "Set intermediate file, where the probes are stored")

  parser.add_argument('--parallel', '-P', type=int, help = "If given, images will be processed with the given number of parallel processes")

  parser.add_argument('--display', '-x', action='store_true', help = "Displays preprocessed images (waits for user keypress)")
  parser.add_argument('--debug', '-q', type=int, help = "Use only the given number of identities")
  parser.add_argument('--force', '-F', action='store_true', help = "If selected, already processed files will be overwritten")


  bob.core.log.add_command_line_option(parser)
  args = parser.parse_args(command_line_arguments)
  bob.core.log.set_verbosity_level(logger, args.verbose)

  if args.parallel is not None and args.display:
    logger.warn("Disabling --display (-x) as we run in parallel mode")
    args.display = False

  if args.debug is not None:
    temp_dir = "temp-%d" % args.debug
    args.training_image_file = args.training_image_file.replace("temp", temp_dir)
    args.projector_file = args.projector_file.replace("temp", temp_dir)
    args.models_file = args.models_file.replace("temp", temp_dir)
    args.probes_file = args.probes_file.replace("temp", temp_dir)
    args.result_file = args.result_file.replace("baseline", "baseline-%d"%args.debug)
  bob.io.base.create_directories_safe(os.path.dirname(args.training_image_file))
  bob.io.base.create_directories_safe(os.path.dirname(args.projector_file))
  bob.io.base.create_directories_safe(os.path.dirname(args.models_file))
  bob.io.base.create_directories_safe(os.path.dirname(args.probes_file))
  bob.io.base.create_directories_safe(os.path.dirname(args.result_file))

  return args

def _display(image, bbxs, args, gts=[]):
  if args.display:
    from matplotlib import pyplot, patches
    pyplot.figure("original")
    pyplot.clf()
    pyplot.imshow(image, 'gray', clim=(0,255))
    for bbx in bbxs:
      pyplot.gca().add_patch(patches.Rectangle((bbx.left, bbx.top), bbx.size[1], bbx.size[0], fill=False, color='g', lw=3))
    for gt in gts:
      pyplot.gca().add_patch(patches.Rectangle((gt.left, gt.top), gt.size[1], gt.size[0], fill=False, color='r', lw=3))
    raw_input("Press Enter to continue")


cropper = bob.ip.base.GeomNorm(0., 1., (80,64), (40,32))
def _align(image, bbx):
  # crop by the bounding box
  # as the images are not aligned inside the bounding box, we crop the center of them
  bbx = utils.bounding_box(bbx)
  center = bbx.center
  # set the scale
  cropper.scaling_factor = min(float(cropper.crop_size[0]) / bbx.size[0], float(cropper.crop_size[1]) / bbx.size[1])
  cropped = numpy.ndarray(cropper.crop_size)
  cropper(image, cropped, center)
  return cropped

def _feature(face):
  """Extracts an LBPHS feature for the given face chip.
  """
  return bob.ip.base.lbphs(face, bob.ip.base.LBP(8,1,uniform=True,border_handling='wrap'), block_size=(16,16)).astype(numpy.float64).flatten()

def _bbx(b,q):
  # turns the BoundingBox C++ object into a (picklable) list so that it can be returned through multiprocessing
  return b.left_f, b.top_f, b.size_f[1], b.size_f[0], q


def _redetect_training_faces(params):
  """Re-detects the faces in the training images -- to be of the same size as we will use later on for the test images"""
  # get process ID
  p = multiprocessing.current_process().name
  process_id = int(p.split('-')[1]) if p != 'MainProcess' else -1

  dataset, args = params
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


  logger.debug("Detecting faces in %d training images%s", len(dataset), (" in process %d" % process_id) if process_id > 0 else "")

  detected_faces = {}
  for image_name in dataset:
    detected_faces[image_name] = []
    # load image and convert to gray scale
    image = bob.io.base.load(os.path.join(args.data_directory, "training", image_name))
    if image.ndim == 3:
      image = bob.ip.color.rgb_to_gray(image)

    # detect all faces, with a low threshold
    detections, qualities = bob.ip.facedetect.detect_all_faces(image, cascade, sampler, 0, 3, 0.25, 0.)

    # iterate over all ground-truth bounding boxes and select the detected ones that have the highest overlap
    for subject, bbx in dataset[image_name]:
      if subject == -1 and args.no_train_on_unknowns:
        continue
      # For the training set:
      # check which of the detected bounding boxes have the best overlap with the GT bounding box
      gt = utils.bounding_box(bbx)
      overlaps = sorted(((utils.overlap(gt, det), det, val) for det, val in zip(detections, qualities)), key=lambda x:x[0], reverse=True)
      if overlaps[0][0] < 0.5:
        # no detected bounding box overlapped with the ground-truth
        logger.warning("Labeled face of training subject %d at location %s in image %s not detected; skipping", subject, gt, image_name)
        continue
      # we take the bounding box with the highest overlap
      detected_faces[image_name].append((subject, _bbx(overlaps[0][1], overlaps[0][2])))

    # display all re-detected faces and the ground truth
    _display(image, [utils.bounding_box(bbx) for subject, bbx in detected_faces[image_name]], args, [utils.bounding_box(bbx) for subject, bbx in dataset[image_name]])

  return detected_faces


def _detect_test_faces(params):
  """Extracts validation or test features and rearranges them by filename"""
  # get process ID
  p = multiprocessing.current_process().name
  process_id = int(p.split('-')[1]) if p != 'MainProcess' else -1

  dataset, args = params
  # load classifier and feature extractor; each process needs its own cascade
  if args.cascade_file is None:
    if abs(process_id) == 1:
      logger.info("Using default frontal face detection cascade from bob.ip.facedetect")
    cascade = bob.ip.facedetect.default_cascade()
  else:
    if abs(process_id) == 1:
      logger.info("Loading cascade from file '%s'", args.cascade_file)
    cascade = bob.ip.facedetect.detector.Cascade(bob.io.base.HDF5File(args.cascade_file))
  # initialize sampler with the options provided on command line
  sampler = bob.ip.facedetect.detector.Sampler(patch_size=cascade.extractor.patch_size, distance=args.distance, scale_factor=args.scale_factor, lowest_scale=args.lowest_scale)

  logger.debug("Detecting faces in %d test images%s", len(dataset), (" in process %d" % process_id) if process_id > 0 else "")

  detected_faces = {}
  # iterate over all images
  for image_name in dataset:
    # load image and convert to gray scale
    image = bob.io.base.load(os.path.join(args.data_directory, "validation", image_name))
    if image.ndim == 3:
      image = bob.ip.color.rgb_to_gray(image)

    # get bounding boxes and their qualities
    faces = bob.ip.facedetect.detect_all_faces(image, cascade, sampler, args.absolute_threshold, args.number_of_overlaps, args.detection_overlap, args.relative_threshold)
    if faces is not None:
      bounding_boxes, qualities = faces

      # sort bbxs and qualities by qualities descendingly
      bounding_boxes, qualities = (list(x) for x in zip(*sorted(zip(bounding_boxes, qualities), key=lambda pair: pair[1], reverse=True)))
    else:
      bounding_boxes, qualities = [], []

    # limit bounding boxes
    bounding_boxes = bounding_boxes[:args.maximum_detections]

    # iterate over all detections
    detected_faces[image_name] = []
    for i, bbx in enumerate(bounding_boxes):
      detected_faces[image_name].append(_bbx(bbx, qualities[i]))

    # display all detected faces
    _display(image, [utils.bounding_box(bbx) for bbx in detected_faces[image_name]], args)

  logger.debug("Finished processing%s" % (" process %d" % process_id) if process_id > 0 else "")
  return detected_faces


def detect_faces(data, pool, args, is_training):
  """Detects the faces in the given images"""
  which = "training" if is_training else "test"
  # select, which function to use for feature extraction
  detector = _redetect_training_faces if is_training else _detect_test_faces
  logger.info("Detecting faces in %d images", len(data))
  # extract LBPHS features for all images
  if pool is None:
    detected_faces = detector((data, args))
  else:
    logger.info("Splitting into %d parallel processes", args.parallel)
    splits = utils.split_data_dict_into_parallel(data, args.parallel, (args,))
    detected_faces = {}
    for detected in pool.imap_unordered(detector, splits):
      for k,v in detected.items():
        if k not in detected_faces:
          detected_faces[k] = []
        detected_faces[k].extend(v)

  return detected_faces


def _extract_training_features(params):
  """Extracts training features from all images and rearranges them by identity"""
  # get process ID
  p = multiprocessing.current_process().name
  process_id = int(p.split('-')[1]) if p != 'MainProcess' else -1

  dataset, args = params
  features = {}
  for image_name in dataset:
    # load image and convert to gray scale
    image = bob.io.base.load(os.path.join(args.data_directory, "training", image_name))
    if image.ndim == 3:
      image = bob.ip.color.rgb_to_gray(image)

    # iterate over all bounding boxes and extract features for bbx
    for subject, bbx in dataset[image_name]:
      # extract the face chip for the best matching bounding box
      cropped = _align(image, bbx)

      # extract LBPHS features and add them to the training set of the current subject
      if subject not in features:
        features[subject] = []
      features[subject].append(_feature(cropped))

  logger.debug("Finished processing%s" % (" process %d" % process_id) if process_id > 0 else "")
  return features



def _extract_test_features(params):
  """Extracts training features from all images and rearranges them by identity"""
  # get process ID
  p = multiprocessing.current_process().name
  process_id = int(p.split('-')[1]) if p != 'MainProcess' else -1

  dataset, args = params
  features = {}
  for image_name in dataset:
    # load image and convert to gray scale
    image = bob.io.base.load(os.path.join(args.data_directory, "validation", image_name))
    if image.ndim == 3:
      image = bob.ip.color.rgb_to_gray(image)

    # iterate over all bounding boxes and extract features for bbxs
    features[image_name] = []
    for bbx in dataset[image_name]:
      # crop face according to bounding box
      cropped = _align(image, bbx)
      # store bounding box and extracted LBPHS feature for image
      features[image_name].append((bbx, _feature(cropped)))

  logger.debug("Finished processing%s" % (" process %d" % process_id) if process_id > 0 else "")
  return features


def extract_features(detections, pool, args, is_training):
  """Extracts several LBPHS features for each bounding box in each image"""
  which = "training" if is_training else "test"
  # select, which function to use for feature extraction
  extractor = _extract_training_features if is_training else _extract_test_features
  logger.info("Extracting %s features from %d images", which, len(detections))
  # extract LBPHS features for all images
  if pool is None:
    features = extractor((detections, args))
  else:
    logger.info("Splitting into %d parallel processes", args.parallel)
    splits = utils.split_data_dict_into_parallel(detections, args.parallel, (args,))
    features = {}
    for extracted in pool.imap_unordered(extractor, splits):
      for k,v in extracted.items():
        if k not in features:
          features[k] = []
        features[k].extend(v)

  return features


def _project(params):
  """Projects the given LBPHS features into the PCA or PCA+LDA subspace"""
  data, matrix, mean = params
  projector = bob.learn.linear.Machine(matrix)
  projector.input_subtract = mean
  return {subject: projector(f) if len(f) else [] for subject, f in data.items()}


def project(projector, data, pool, args):
  """Projects all LBPHS features into the PCA or PCA+LDA subspace"""
  if pool is None:
    return _project((data, projector.weights, projector.input_subtract))
  else:
    logger.info("Splitting into %d parallel processes", args.parallel)
    data_splits = utils.split_data_dict_into_parallel(data, args.parallel, (projector.weights, projector.input_subtract))
    projected = {}
    for p in pool.imap_unordered(_project, data_splits):
      projected.update(p)
    return projected


def train_pca_lda(training_features, pool, args):
  """Trains a combined PCA+LDA projection matrix from the given LBPHS features from the training set"""
  # build a single data structure of the features
  data = numpy.vstack(training_features.values())
  logger.info("Training PCA with %d features of dimension %d", *data.shape)
  # first, train a PCA projection matrix
  trainer = bob.learn.linear.PCATrainer()
  pca, eigen_values = trainer.train(data)

  # compute relative energy of eigenvalues
  cumulated = numpy.cumsum(eigen_values) / numpy.sum(eigen_values)
  # compute number of eigenvalues so that the cumulated energy is larger than the one specified on command line
  pca_subspace = numpy.searchsorted(cumulated, args.eigenvalue_energy, side='right')
  # limit number of pcs
  pca.resize(pca.shape[0], pca_subspace)

  # project LBPHS features into PCA subpaces
  logger.info("Projecting training features into PCA subspace of size %d", pca_subspace)
  projected_pca = project(pca, training_features, pool, args)

  logger.info("Training LDA using %d subjects", len(projected_pca))
  trainer = bob.learn.linear.FisherLDATrainer(use_pinv = True, strip_to_rank = True)
  lda, variances = trainer.train(projected_pca.values())
  logger.info("Final LDA subspace size %s", lda.shape[1])

  # project training features into LDA subspace
  projected_lda = project(lda, projected_pca, pool, args)

  logger.info("Computing combined PCA+LDA projection matrix")
  combined_matrix = numpy.dot(pca.weights, lda.weights)
  projector = bob.learn.linear.Machine(combined_matrix)
  projector.input_subtract = pca.input_subtract

  # write into file
  logger.info("Writing data into %s", args.projector_file)
  h = bob.io.base.HDF5File(args.projector_file, 'w')
  h.create_group("Projector")
  h.create_group("Projected")
  h.cd("Projector")
  projector.save(h)
  h.cd("../Projected")
  for f,v in projected_lda.items():
    h.set(str(f),v)
  return projector, projected_lda

def read_projector(args):
  logger.info("Reading data from %s", args.projector_file)
  h = bob.io.base.HDF5File(args.projector_file, 'r')
  h.cd("Projector")
  projector = bob.learn.linear.Machine(h)
  h.cd("../Projected")
  projected = {int(f):h.get(f) for f in h.keys(relative=True)}
  return projector, projected


def _compare(model, probe):
  return - scipy.spatial.distance.euclidean(model, probe)

def _scores(arguments):
  probes, models, args  = arguments
  scores_for_probes = {}
  for image, probe_features in probes.items():
    scores_for_probes[image] = []
    scores = {}
    for probe in probe_features:
      for subject, model in models.items():
        scores[subject] = _compare(model, probe)
      # keep only maximum scores
      lowest_score = sorted(scores.values())[-args.maximum_scores]
      if -1 in scores:
        # when we predict -1 in our scores, the -1 score should be the lowest to be written
        lowest_score = max(lowest_score, scores[-1])
      scores_for_probes[image].append({subject : score for subject,score in scores.items() if score >= lowest_score})
  return scores_for_probes


def compute_scores(models, probes, pool, args):
  logger.info("Computing scores between %s models and %d probes", len(models), len(probes))
  # extract training features
  if pool is None:
    scores = _scores((probes, models, args))
  else:
    logger.info("Splitting into %d parallel processes", args.parallel)
    probe_splits = utils.split_data_dict_into_parallel(probes, args.parallel, (models, args))
    scores = {}
    for score in pool.imap_unordered(_scores, probe_splits):
      scores.update(score)

  return scores

def limit(data, subjects, use_unknowns):
  tmp = {}
  unknown_counter = 0
  max_unknowns = len(subjects) * 10
  for f,v in data.items():
    if use_unknowns and v[0][0] == -1 and unknown_counter < max_unknowns:
      tmp[f] = v
      unknown_counter += 1
    elif v[0][0] in subjects:
      tmp[f] = v
  return tmp


def main(command_line_arguments = None):

  # get command line arguments
  args = command_line_options(command_line_arguments)

  # for the training set, we use all available data
  training = utils.read_ground_truth(args.data_directory, "training")
  # for the validation set, we will use only the image names
  validation = utils.read_ground_truth(args.data_directory, "validation")

  if args.debug is not None:
    subjects = set(range(1,args.debug+1))
    training = limit(training, subjects, not args.no_train_on_unknowns)
    validation = limit(validation, subjects, True)
    logger.info("Limited to %d training and %d validation images of %d subjects", len(training), len(validation), len(subjects))

  pool = None if args.parallel is None else multiprocessing.Pool(args.parallel)

  if not os.path.exists(args.projector_file) or args.force:
    if not args.no_redetect_training_images:
      if not os.path.exists(args.training_image_file) or args.force:
        # re-detect training faces; this might take some time
        training_detections = detect_faces(training, pool, args, is_training=True)
        # write them to file
        h = bob.io.base.HDF5File(args.training_image_file, 'w')
        for image_name, bbxs in training_detections.items():
          h.create_group(image_name)
          h.cd(image_name)
          h.set("Identities", numpy.array([identity for identity, bbx in bbxs]))
          h.set("BoundingBoxes", numpy.array([bbx for identity, bbx in bbxs]))
          h.cd('..')
      else:
        # read them from file
        h = bob.io.base.HDF5File(args.training_image_file)
        training_detections = {}
        for image_name in h.sub_groups(relative=True, recursive=False):
          h.cd(image_name)
          identities = h.lread("Identities")
          bbxs = h.lread("BoundingBoxes")
          training_detections[image_name] = zip(identities, bbxs)
          h.cd('..')
    else:
      # if no redetection is desired, use the originally labeled bounding boxes
      logger.warn("Using hand-labeled training set bounding boxes -- this is **not recommended**")
      training_detections = training

    # extract training features
    training_features = extract_features(training_detections, pool, args, is_training=True)

    # train PCA+LDA on training features
    projector, projected_training_data = train_pca_lda(training_features, pool, args)
  else:
    projector, projected_training_data = read_projector(args)

  if not os.path.exists(args.models_file) or args.force:
    # enroll models from training set images
    models = {subject : numpy.mean(features, axis=0) for subject, features in projected_training_data.items()}
    logger.info("Writing models to file %s", args.models_file)
    h = bob.io.base.HDF5File(args.models_file, 'w')
    for subject, model in models.items():
      h.set(str(subject), model)
  else:
    logger.info("Reading models from file %s", args.models_file)
    h = bob.io.base.HDF5File(args.models_file, 'r')
    models = {int(f): h.get(f) for f in h.keys(relative=True)}



  if not os.path.exists(args.probes_file) or args.force:
    # now, get validation features
    if args.detector_result_file is None:
      # detect test faces; this might take some time
      validation_detections = detect_faces(validation, pool, args, is_training=False)
    else:
      # read the detections from detector result file
      logger.info("Using validation set detections from '%s'", args.detector_result_file)
      validation_detections = utils.read_detections(args.detector_result_file)
      if args.debug is not None:
        validation_detections = {k:v for k,v in validation_detections.items() if k in validation}
      # get it in the same data structure as when detecting them ourselves
      validation_detections = {k:[list(b)+[d] for (b,d) in v] for k,v in validation_detections.items()}

    validation_features = extract_features(validation_detections, pool, args, is_training=False)

    # align features to be projected
    bounding_boxes = {image : [feature[0] for feature in val] for image, val in validation_features.items()}
    features = {image : [feature[1] for feature in val] for image, val in validation_features.items()}

    # and project them
    logger.info("Projecting features from %d images", len(features))
    probes = project(projector, features, pool, args)

    logger.info("Writing probes from %d images to file %s", len(probes), args.probes_file)
    h = bob.io.base.HDF5File(args.probes_file, 'w')
    for filename, probe in probes.items():
      h.set(filename.replace("/","$"), probe)
      h.set(filename.replace("/","$")+"-bbxs", bounding_boxes[filename])

  else:
    logger.info("Reading probes from file %s", args.probes_file)
    h = bob.io.base.HDF5File(args.probes_file, 'r')
    probes = {f.replace("$","/"): h.get(f) for f in h.keys(relative=True) if '-bbxs' not in f}
    bounding_boxes = {f.replace("$","/").replace("-bbxs",""): h.get(f) for f in h.keys(relative=True) if '-bbxs' in f}


  # compute similarities between model and probes
  scores = compute_scores(models, probes, pool, args)

  logger.info("Writing scores to score file %s", args.result_file)
  bob.io.base.create_directories_safe(os.path.dirname(args.result_file))
  with open(args.result_file, 'w') as f:
    if command_line_arguments is None:
      import sys
      command_line_arguments = sys.argv
    f.write("# Created using command line: %s\n" % " ".join(command_line_arguments))
    f.write("# FILE,BB_X,BB_Y,BB_WIDTH,BB_HEIGHT,DETECTION_SCORE,SUBJECT_ID_1,RECOGNITION_SCORE_1,SUBJECT_ID_2,RECOGNITION_SCORE_2,SUBJECT_ID_3,RECOGNITION_SCORE_3,...\n")
    for probe_image in sorted(scores.keys()):
      for p, values in enumerate(scores[probe_image]):
        bbx = bounding_boxes[probe_image][p]
        f.write("%s,%3.2f,%3.2f,%3.2f,%3.2f,%3.2f" % (probe_image, bbx[0], bbx[1], bbx[2], bbx[3], bbx[4]))
        for subject, value in values.items():
          f.write(",%d,%3.2f" % (subject, value))
        f.write("\n")
