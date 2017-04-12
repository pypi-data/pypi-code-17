import csv
import os

import logging
logger = logging.getLogger("challenge.UCCS")

def _extract(splits):
  if len(splits) == 1:
    # test set file; we do not know anything about subject id or bounding box
    return splits[0], None, None

  assert len(splits) == 7
  image = splits[1]
  subject = int(splits[2])
  bbx = [float(v) for v in splits[3:7]] # left, top, width, height
  return image, subject, bbx

def read_ground_truth(data_directory, stage):
  """Reads ground truth bounding boxes of the training and validation set for the given dataset.
  For the test set, it only reads the image names as keys of the dictionary; the values are ``None``."""
  data = {}
  protocol_file = os.path.join(data_directory, "protocol", "%s.csv" % stage)
  if not os.path.exists(protocol_file):
    raise ValueError("The protocol file '%s.csv' seems not to be in the expected directory '%s'" % (stage, protocol_file))
  with open(protocol_file) as list_file:
    # skip header
    list_file.readline()
    reader = csv.reader(list_file)
    # read line by line
    for splits in reader:
      image, subject, bbx = _extract(splits)
      if image not in data:
        data[image] = []
      # debug: find issues with the protocol files
      if subject != -1:
        ids = set(s for s,_ in data[image])
        if subject in ids:
          logger.warning("ID %d (face_id %s) is already labeled in image %s", subject, splits[0], image)
      data[image].append((subject, bbx))
  return data



def _result(splits):
  if len(splits) < 6 or len(splits) % 2 != 0:
    logger.error("Cannot interpret score file line '%s'" % ",".join(splits))

  image = splits[0]
  bbx = [float(v) for v in splits[1:5]] # left, top, width, height
  fd_quality = float(splits[5])
  scores = {int(splits[i]) : float(splits[i+1]) for i in range(6, len(splits), 2)} # scores in order id1, score1, id2, score2, ...

  return image, bbx, fd_quality, scores


def read_detections(result_file):
  """Reads the csv file for the face detections and sorts them by file."""
  if not os.path.exists(result_file):
    raise ValueError("The score file '%s' does not exist" % result_file)
  data = {}
  with open(result_file) as data_file:
    reader = csv.reader(data_file)
    for splits in reader:
      if not len(splits) or splits[0][0] == "#":
        continue
      image, bbx, q, _ = _result(splits)
      if image not in data:
        data[image] = []
      data[image].append((bbx, q))
  return data


def read_recognitions(result_file, header_lines = 2):
  """Reads the csv file with the face recognition results and sorts them by file."""
  if not os.path.exists(result_file):
    raise ValueError("The score file '%s' does not exist" % result_file)
  data = {}
  with open(result_file) as data_file:
    # read data line by line
    reader = csv.reader(data_file)
    for splits in reader:
      if not len(splits) or splits[0][0] == "#":
        # skip empty lines or lines with
        continue
      image, bbx, q, scores = _result(splits)
      if image not in data:
        data[image] = []
      data[image].append((bbx, scores))
  return data
