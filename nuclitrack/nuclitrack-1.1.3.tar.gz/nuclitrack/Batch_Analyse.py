import platform
import h5py
from skimage.measure import regionprops
import tracking_c_tools
import argparse
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import multiprocessing
from multiprocessing import Pool
from functools import partial
from skimage import filters
from skimage import morphology
from skimage.feature import peak_local_max
from skimage.external import tifffile
from scipy import ndimage
import os
import segmentation_c_tools

parser = argparse.ArgumentParser(description='Batch Analysis')
parser.add_argument('--txtfile', dest = 'text_file')
parser.add_argument('--paramfile', dest='param_file')
parser.add_argument('--outputdir', dest='output_dir')

args = parser.parse_args()

# Functions for segmentation

def clipping(im, val):

    im_temp = im.copy()

    if val != 0:
        im_temp[im > val] = val

    return im_temp

def background(im, val):

    im_temp = im.copy()

    if val != 0:
        im_temp = im_temp - segmentation_c_tools.fast_blur(im_temp, val)

    return im_temp


def blur(im, val):

    if val != 0:

        if val <= 5:
            im = filters.gaussian(im, val)

        else:

            im = filters.gaussian(im, (val / 2))
            im = filters.gaussian(im, (val / 2))
            im = filters.gaussian(im, (val / 2))

    im = im/np.max(im.flatten())

    return im


def threshold(im, val):

    im_bin = im > val

    return im_bin


def object_filter(im_bin, val):

    im_bin = morphology.remove_small_objects(im_bin, val)

    return im_bin


def cell_centers(im, im_bin, val):

    d_mat = ndimage.distance_transform_edt(im_bin)
    d_mat = d_mat / np.max(d_mat.flatten())

    im_cent = (1 - val) * im + val * d_mat
    im_cent[np.logical_not(im_bin)] = 0

    return [im_cent, d_mat]


def fg_markers(im_cent, im_bin, val, edges):

    local_maxi = peak_local_max(im_cent, indices=False, min_distance=int(val), labels=im_bin, exclude_border=int(edges))
    markers = ndimage.label(local_maxi)[0]
    markers[local_maxi] += 1
    k = morphology.octagon(2, 2)
    markers = morphology.dilation(markers, selem=k)

    return markers

def sobel_edges(im, val):

    if val != 0:
        if val <= 5:
            im = filters.gaussian(im, val)

        else:

            im = filters.gaussian(im, (val / 2))
            im = filters.gaussian(im, (val / 2))
            im = filters.gaussian(im, (val / 2))

    im = filters.sobel(im) + 1
    im = im / np.max(im.flatten())

    return im


def watershed(markers, im_bin, im_edge, d_mat, val, edges):

    k = morphology.octagon(2, 2)
    im_bin = morphology.binary_dilation(im_bin, selem=k)
    im_bin = morphology.binary_dilation(im_bin, selem=k)

    markers_temp = markers + np.logical_not(im_bin)
    im_bin = morphology.binary_dilation(im_bin, selem=k)
    shed_im = (1 - val) * im_edge - val * d_mat

    labels = morphology.watershed(image=shed_im, markers=markers_temp, mask=im_bin)
    labels -= 1
    if edges == 1:
        edge_vec = np.hstack((labels[:, 0].flatten(), labels[:, -1].flatten(), labels[0, :].flatten(),
                              labels[-1, :].flatten()))
        edge_val = np.unique(edge_vec)
        for val in edge_val:
            if not val == 0:
                labels[labels == val] = 0

    return labels

def segment_image(params, image):

    image = clipping(image, params[0])
    image2 = background(image, params[1])
    image3 = blur(image2, params[2])
    im_bin = threshold(image3, params[3])
    im_bin = object_filter(im_bin, params[4])
    [cell_center, d_mat] = cell_centers(image3, im_bin, params[5])
    markers = fg_markers(cell_center, im_bin, params[6], params[9])
    im_edge = sobel_edges(image, params[7])
    return watershed(markers, im_bin, im_edge, d_mat, params[8], params[9])

def classify_cells(features, training_data):

    training_data = np.delete(training_data, 0, 0)
    clf = RandomForestClassifier(n_estimators=100)
    mask = np.sum(training_data[:, 12:17], axis=0) > 0

    if sum(mask) > 1:
        inds = np.where(mask)[0]
        clf = clf.fit(training_data[:, 5:10], training_data[:, 12 + inds].astype(bool))
        probs = clf.predict_proba(features[:, 5:10])

        i = 0
        for p in probs:
            if len(p[0]) == 1:
                p = np.hstack([np.asarray(p), np.zeros((len(p), 1))])
            else:
                p = np.asarray(p)

            features[:, 12 + inds[i]] = p[:, 1]
            i += 1

    if sum(mask) == 1:
        ind = np.where(mask)[0]
        features[:, 12 + ind] = 1

    return features

def extract_features(images, labels, frames):
    channels = len(images)
    feature_num = 20 + 3 * (channels - 1)
    counter = 1
    dims = images[0].shape
    features = np.zeros([1, feature_num])

    for i in range(frames):

        img_label = labels[i, :, :].copy()
        features_temp = []

        for j in range(channels):
            features_temp.append(regionprops(img_label, images[j][i, :, :]))

        feature_mat = np.zeros((len(features_temp[0]), feature_num))
        img_new = np.zeros(img_label.shape)

        for j in range(len(features_temp[0])):

            cell_temp = features_temp[0][j]

            features_vector = np.zeros(feature_num)

            ypos = cell_temp.centroid[0]
            xpos = cell_temp.centroid[1]

            features_vector[0] = counter
            features_vector[1] = i
            features_vector[2] = xpos
            features_vector[3] = ypos
            features_vector[4] = min([ypos, dims[1] - ypos, xpos, dims[2] - xpos])

            features_vector[5] = cell_temp.area
            features_vector[6] = cell_temp.eccentricity
            features_vector[7] = cell_temp.major_axis_length
            features_vector[8] = cell_temp.perimeter

            mu = cell_temp.mean_intensity
            im_temp = cell_temp.intensity_image.flatten()
            bin_temp = cell_temp.image.flatten()
            im_temp = im_temp[bin_temp]

            features_vector[9] = mu
            features_vector[10] = np.std(im_temp)
            features_vector[11] = np.std(im_temp[im_temp > mu])

            for k in range(1, channels):
                cell_temp = features_temp[k][j]

                mu = cell_temp.mean_intensity
                im_temp = cell_temp.intensity_image.flatten()
                bin_temp = cell_temp.image.flatten()
                im_temp = im_temp[bin_temp]

                features_vector[20 + (k - 1) * 3 + 0] = mu
                features_vector[20 + (k - 1) * 3 + 1] = np.std(im_temp)
                features_vector[20 + (k - 1) * 3 + 2] = np.std(im_temp[im_temp > mu])

            feature_mat[j, :] = features_vector
            img_new[img_label == cell_temp.label] = counter

            counter += 1

        features = np.vstack((features, feature_mat))
        labels[i, :, :] = img_new

    return labels, features

def load_images(text_file):

    if os.path.isfile(text_file):

        if platform.system() == 'Windows':
            file_name_split = text_file.split('\\')
            file_name_split = [s + '\\' for s in file_name_split]
        else:
            file_name_split = text_file.split('/')
            file_name_split = [s + '/' for s in file_name_split]

        dir_name = ''.join(file_name_split[:-1])
        file_list = []
        with open(text_file) as f:
            for line in f:
                if line[-1] == '\n':
                    line = line[:-1]
                file_list.append(dir_name + line)
        return file_list


def load_movie(image_filenames, fov):

    # Load images from first channel

    frames = len(image_filenames[0])
    im_test = tifffile.imread(image_filenames[0][0])
    dims = im_test.shape

    images = []
    images_np = []

    for all_image_files in image_filenames:

        all_images = np.zeros((frames, dims[0], dims[1]))

        for i in range(len(all_image_files)):
            im_temp = tifffile.imread(all_image_files[i])
            im_temp = im_temp.astype(float)
            all_images[i, :, :] = im_temp

        images.append(all_images)

        # Transform file names to bytes for storing in hdf5 file
        images_np.append([bytes(image_file, encoding='utf8') for image_file in all_image_files])

    images_np = np.asarray(images_np)

    for i in range(len(images)):
        images[i] = images[i] / np.max(images[i].flatten())

    fov.create_dataset('image_filenames', data=images_np)

    return images

def track_cells(features, frames, track_param):

    features[:, 18] = 1
    features = np.vstack((np.zeros((1, features.shape[1])), features))

    states = np.zeros(features.shape[0], dtype=int)
    tracks = np.zeros([1, 8])

    d_mat = tracking_c_tools.distance_mat(features, frames, track_param)
    d_mat = d_mat[d_mat[:, 2].argsort(), :]
    d_mat = np.vstack((d_mat, np.zeros((1, d_mat.shape[1]))))
    s_mat = tracking_c_tools.swaps_mat(d_mat, frames)

    cum_score = 0.
    count = 1
    min_score = 5
    max_score = min_score+1

    print('Tracking Cells')

    while max_score > min_score:

        print(max_score)
        score_mat = tracking_c_tools.forward_pass(features, d_mat, s_mat, states, track_param)
        max_score = max(score_mat[:, 3])

        if max_score > min_score:

            cum_score += max_score
            track_temp, s_mat, states = tracking_c_tools.track_back(score_mat, states, s_mat)
            track_temp[:, 4] = count

            tracks, track_temp = tracking_c_tools.swap_test(tracks, track_temp, d_mat, count)

            tracks = np.vstack((tracks, track_temp))
            count += 1

    print('Optimising Tracks')

    for h in range(2):
        for i in range(np.max(tracks[:, 4])):

            print(i)
            replace_mask = tracks[:, 4] == i
            track_store = tracks[replace_mask, :]

            tracks = tracks[np.logical_not(replace_mask), :]

            for j in range(track_store.shape[0]):  # Remove track

                states[int(track_store[j, 0])] -= 1

                if j > 0:

                    ind1 = track_store[j - 1, 0]
                    ind2 = track_store[j, 0]

                    m1 = np.logical_and(s_mat[:, 1] == ind1, s_mat[:, 3] == ind2)
                    m2 = np.logical_and(s_mat[:, 2] == ind1, s_mat[:, 3] == ind2)
                    m3 = np.logical_and(s_mat[:, 1] == ind1, s_mat[:, 4] == ind2)
                    m4 = np.logical_and(s_mat[:, 2] == ind1, s_mat[:, 4] == ind2)

                    if any(m1):
                        s_mat[m1, 5] = 0
                        s_mat[m1, 7] = 0
                    if any(m2):
                        s_mat[m2, 6] = 0
                        s_mat[m2, 7] = 0
                    if any(m3):
                        s_mat[m3, 5] = 0
                        s_mat[m3, 8] = 0
                    if any(m4):
                        s_mat[m4, 6] = 0
                        s_mat[m4, 8] = 0

            score_mat = tracking_c_tools.forward_pass(features, d_mat, s_mat, states, track_param)
            max_score = max(score_mat[:, 3])

            if max_score > track_store[-1, 2]:

                cum_score = cum_score + max_score - track_store[-1, 2]
                track_replace, s_mat, states = tracking_c_tools.track_back(score_mat, states, s_mat)
                track_replace[:, 4] = i

                tracks, track_replace = tracking_c_tools.swap_test(tracks, track_replace, d_mat, i)
                tracks = np.vstack((tracks, track_replace))

            else:
                tracks = np.vstack((tracks, track_store))

                for j in range(track_store.shape[0]):

                    states[int(track_store[j, 0])] += 1

                    if j > 0:

                        ind1 = track_store[j - 1, 0]
                        ind2 = track_store[j - 1, 0]

                        m1 = np.logical_and(s_mat[:, 1] == ind1, s_mat[:, 3] == ind2)
                        m2 = np.logical_and(s_mat[:, 2] == ind1, s_mat[:, 3] == ind2)
                        m3 = np.logical_and(s_mat[:, 1] == ind1, s_mat[:, 4] == ind2)
                        m4 = np.logical_and(s_mat[:, 2] == ind1, s_mat[:, 4] == ind2)

                        if any(m1):
                            s_mat[m1, 5] = 1
                            s_mat[m1, 7] = 1
                        if any(m2):
                            s_mat[m2, 6] = 1
                            s_mat[m2, 7] = 1
                        if any(m3):
                            s_mat[m3, 5] = 1
                            s_mat[m3, 8] = 1
                        if any(m4):
                            s_mat[m4, 6] = 1
                            s_mat[m4, 8] = 1

    tracks[:, 0] = tracks[:, 0] - 1
    unique, counts = np.unique(tracks[:, 0], return_counts=True)

    double_seg = unique[counts > 1]
    for val in double_seg:
        tracks = tracks[np.logical_not(tracks[:, 0] == val), :]

    return tracks, features

def csv_export(features, tracks, output_dir):

    if features.shape[1] == 20:
        features = np.hstack((features, np.zeros((features.shape[0], 6))))

    if features.shape[1] == 23:
        features = np.hstack((features, np.zeros((features.shape[0], 3))))

    feat_mat = np.zeros((1, 20))

    for i in range(1, int(max(tracks[:, 4])) + 1):
        if sum(tracks[:, 4] == i) > 0:

            track_temp = tracks[tracks[:, 4] == i, :]

            for j in range(track_temp.shape[0]):
                mask = features[:, 0] == track_temp[j, 0]
                fv = features[mask, :]
                feat_mat = np.vstack((feat_mat,
                                      [i, track_temp[j, 5], fv[0, 2], fv[0, 3], fv[0, 5], fv[0, 6], fv[0, 7],
                                       fv[0, 8], fv[0, 9], fv[0, 10], fv[0, 11], fv[0, 20], fv[0, 21],
                                       fv[0, 22], fv[0, 23], fv[0, 24], fv[0, 25], track_temp[j, 3],
                                       track_temp[j, 0], 0]))

    feat_mat = np.delete(feat_mat, 0, 0)

    for i in range(feat_mat.shape[0]):

        if feat_mat[i, 17] > 0:

            mask = feat_mat[:, 18] == feat_mat[i, 17]
            ind_change = feat_mat[mask, 0]

            frame_change = feat_mat[mask, 1]
            mask_change = np.logical_and(feat_mat[:, 0] == ind_change, feat_mat[:, 1] > frame_change)
            if sum(mask_change) > 0:
                change_list = np.where(mask_change)
                feat_mat[change_list[0][0], 19] = ind_change
                feat_mat[i, 19] = ind_change

    with open(output_dir + 'results.csv', 'wb') as f:
        f.write(b'Track ID, Frame, X center, Y center, Area, Eccentricity, Solidity, Perimeter, '
                b'CH1 Mean Intensity, CH1 StdDev Intensity, CH1 Floored Mean, CH2 Mean Intensity, '
                b'CH2 StdDev Intensity, CH3 Mean Intensity, CH3 StdDev Intensity, Parent Track ID\n')

        feat_mat2 = np.delete(feat_mat, [17, 18], 1)
        np.savetxt(f, feat_mat2, delimiter=",", fmt='%10.4f')


def batch_analyse(text_file=None, param_file=None, output_dir=None):

    print('Loading Images')
    fov = h5py.File(output_dir+'output.h5py', "a")
    file_list = load_images(text_file)
    images = load_movie(file_list, fov)
    params = h5py.File(param_file, "a")
    s_params = params['seg_param'][...]
    frames = images[0].shape[0]

    print('Segmenting Cells')
    cpu_count = multiprocessing.cpu_count()
    pool = Pool(cpu_count)
    labels = pool.map(partial(segment_image, s_params), [images[0][frame, :, :] for frame in range(frames)])
    pool.close()
    pool.join()
    fov.create_dataset("labels", data=labels)

    print('Extracting features')
    labels, features = extract_features(images, labels, frames)

    features = classify_cells(features, params['training_data'][...])
    tracks, features = track_cells(features, frames, [0.05, 50, 1, 5, 0, 1, 3])

    fov.create_dataset("features")
    fov.create_dataset("tracks", data=tracks)

    tracks_stored = np.zeros(int(max(tracks[:, 4])))
    fov.create_dataset("tracks_stored", data=tracks_stored)

    csv_export(features, tracks, output_dir)

batch_analyse(text_file=args.text_file, param_file=args.param_file, output_dir=args.output_dir)




