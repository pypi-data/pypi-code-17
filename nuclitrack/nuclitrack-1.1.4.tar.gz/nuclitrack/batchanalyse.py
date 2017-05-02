import h5py
import argparse
import numpy as np
import multiprocessing
from multiprocessing import Pool
from functools import partial

from . import loadimages
from . import extractfeatures
from . import classifycells
from . import segmentimages
from . import trackcells

parser = argparse.ArgumentParser(description='Batch Analysis')
parser.add_argument('--txtfile', dest = 'text_file')
parser.add_argument('--paramfile', dest='param_file')
parser.add_argument('--outputdir', dest='output_dir')

args = parser.parse_args()


def add_track(self):

    if self.add_flag:

        self.add_flag =
        self.count += 1

        if not self.add_flag:
            self.optimise_flag = True
            self.update_message(self.sweep + 1)

        return False

    if self.optimise_flag:

        self.optimise_flag = self.tracking_object.optimisetrack()
        self.optimise_count += 1

        if not self.optimise_flag and self.sweep < 1:
            self.optimise_count = 0
            self.sweep += 1
            self.update_message(self.sweep + 1)
            self.optimise_flag = True

        return False

    if not self.add_flag and not self.optimise_flag:
        self.optimise_count = 0
        self.tracks, self.features, self.segment_count, self.double_segment = self.tracking_object.get()
        self.update_message(-1)

        return True

def batch_analyse(text_file=None, param_file=None, output_dir=None):

    print('Loading Images')
    fov = h5py.File(output_dir+'output.h5py', "a")

    file_list = loadimages.filelistfromtext(text_file)
    loadimages.savefilelist(file_list, fov)

    images = loadimages.loadimages(file_list)
    channel_num = len(images)
    params = h5py.File(param_file, "a")
    s_params = params['seg_param'][...]
    frames = images[0].shape[0]

    print('Segmenting Cells')
    cpu_count = multiprocessing.cpu_count()
    pool = Pool(cpu_count)
    labels = pool.map(partial(segmentimages.segment_image, s_params), [images[0][frame, :, :] for frame in range(frames)])
    pool.close()
    pool.join()
    fov.create_dataset("labels", data=labels)

    print('Extracting features')
    feature_num = 20 + 3 * (channel_num - 1)
    for i in range(frames):

        feature_images = [labels[i, :, :]]
        for j in range(channel_num):
            feature_images.append(images[j][i, :, :])

        labels, features = extractfeatures.framefeatures(feature_images, feature_num, i)

    features = classifycells.classifycells(features, params['training_data'][...])

    tracking_object = trackcells.TrackCells(features, frames, [0.05, 50, 1, 5, 0, 1, 3])

    print('Tracking cells')
    counter = 0
    while tracking_object.addtrack():
        counter += 1
        print(counter)

    print('Optimising tracks')
    for i in range(2):
        counter = 0
        while tracking_object.optimisetrack():
            counter += 1
            print(counter)

    tracks, features = tracking_object.get()

    fov.create_dataset("features")
    fov.create_dataset("tracks", data=tracks)

    tracks_stored = np.zeros(int(max(tracks[:, 4])))
    fov.create_dataset("tracks_stored", data=tracks_stored)

    trackcells.save_csv(features, tracks, output_dir)

batch_analyse(text_file=args.text_file, param_file=args.param_file, output_dir=args.output_dir)




