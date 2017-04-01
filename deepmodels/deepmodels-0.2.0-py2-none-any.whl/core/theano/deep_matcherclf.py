'''
deep model for matching images
use metric loss, e.g. triplet loss
but in combination with classification loss to speedup training
and allow class prediction at test time

'''

import sys
import time
import random

import theano
import theano.tensor as T

import lasagne
from lasagne.layers import DenseLayer
from lasagne.nonlinearities import softmax

from core.theano.common import LossType, TripletDist, TripletType, InputDataFormat
from core.theano.base_model import TrainParamsBase, ModelParamsBase, BaseModel, ExptConfigBase
from core.theano.data_manager import gen_rand_cls_combs, gen_triplet_from_cls_combs
from core.theano.model_factory import ModelFactory
from core.theano.search_tools import *


class TripletClfLossTrainParams(TrainParamsBase):
    loss_type = LossType.TripletClassification
    triplet_margin = 0.2
    triplet_mode = TripletType.Random
    triplet_dist = TripletDist.L1
    num_triplets = 100
    extra_info = ''


class MatchClfModelParams(ModelParamsBase):
    # triplet_layer_name should correspond to a features or hash layer
    triplet_layer_name = 'output'
    class_layer_name = 'class'
    class_prev_layer_name = triplet_layer_name


class DeepMatcherClfExptConfig(ExptConfigBase):
    db_name = ''
    loss_name = ''
    extra_info = ''
    base_savedir = ''

    def fill_params(self):
        self.train_params.model_fn_prefix = '{}matcherclf_{}_{}_{}'.format(self.base_savedir,
                                                                           self.db_name,
                                                                           self.loss_name,
                                                                           self.extra_info)
        self.train_params.model_fn = self.train_params.model_fn_prefix + '.pkl'


class DeepMatcherClf(BaseModel):
    def build_model(self):
        self.net = ModelFactory().build_model(self.model_params.model_type,
                                                    self.model_params.img_sz)
        self.net[self.model_params.class_layer_name] = DenseLayer(self.net[self.model_params.class_prev_layer_name],
                                                                  num_units=self.model_params.cls_num,
                                                                  nonlinearity=softmax)

    def create_iter_train_func(self, lrate):
        baseprint = "[DeepMatcherClf.create_iter_train_func] "
        if self.train_params.loss_type != LossType.TripletClassification:
            raise ValueError(baseprint+"ERROR: Incorrect loss type: {}".format(self.train_params.loss_type))

        # compute classification loss
        target_var = T.ivector('train_targets')
        train_output = lasagne.layers.get_output(self.net[self.model_params.class_layer_name])
        class_loss = lasagne.objectives.categorical_crossentropy(train_output, target_var).mean()

        # output are stacked: repeating (anchor, positive, negative)
        # compute anchor-positive and anchor-negative distances
        output = lasagne.layers.get_output(self.net[self.model_params.triplet_layer_name])
        if hasattr(self.train_params, 'triplet_dist') and self.train_params.triplet_dist == TripletDist.L1:
            # L1
            dist1 = (abs(output[::3] - output[1::3])).sum(axis=1) / output.shape[1]
            dist2 = (abs(output[::3] - output[2::3])).sum(axis=1) / output.shape[1]
        else:
            # L2
            output = output / output.norm(2, axis=1).reshape((output.shape[0], 1))
            dist1 = ((output[::3] - output[1::3]) ** 2).sum(axis=1)
            dist2 = ((output[::3] - output[2::3]) ** 2).sum(axis=1)
        # compute triplet loss
        dist = dist1 - dist2 + self.train_params.triplet_margin
        samp_sgn = T.gt(dist, 0.0)
        triplet_loss = T.sum(dist * samp_sgn) / T.shape(output)[0] * 3

        # updates for training
        params = lasagne.layers.get_all_params(self.net[self.model_params.class_layer_name],
                                               trainable=True)
        nb_params = lasagne.layers.count_params(self.net[self.model_params.class_layer_name])
        print(baseprint+"INFO: Total trainable parameter number: {}".format(nb_params))
        updates = lasagne.updates.nesterov_momentum(class_loss + triplet_loss,
                                                    params,
                                                    learning_rate=lrate,
                                                    momentum=0.9)
        start_comp = time.time()
        print(baseprint+"INFO: Start compilation of train function.")
        train_fn = theano.function([self.net['input'].input_var, target_var],
                                   class_loss + triplet_loss,
                                   updates=updates,
                                   name="train_triplet_clf")
        print(baseprint+"INFO: Train function compilation took: {}s.".format(time.time() - start_comp))
        return train_fn

    def learn_model(self, train_data, train_labels, large_scale=False):
        """ Train a model with triplet loss using image filenames as input.

        :param train_data: list of all training images (filenames if large_scale is True)
        :param train_labels: list of all training images labels
        :param large_scale: if True input is supposed to be filenames, image data otherwise
        :return:
        """
        # Initialize
        baseprint = "[DeepMatcherClf.learn_model] "
        if 'train' not in self.iter_funcs:
            self.create_iter_funcs(self.train_params.lrate)
        lrate = self.train_params.lrate
        train_data = np.asarray(train_data)
        total_batches = 0
        total_loss = 0

        # One epoch iterates over the whole dataset
        for epoch in range(self.train_params.num_epochs):
            epoch_startt = time.time()

            # Adjust learning rate every self.train_params.step_lr epoch
            if np.mod(epoch, self.train_params.step_lr) == 0 and epoch > 0:
                lrate = self.train_params.gamma_lr * lrate
                print(baseprint + "INFO: Learning rate is now {}".format(lrate))
                self.create_iter_funcs(lrate)

            # Prepare data and labels
            ids = range(len(train_labels))
            np.random.shuffle(ids)
            input = np.asarray([train_data[id] for id in ids])
            labels = np.asarray([train_labels[id] for id in ids])
            # generate this epoch class pairs, 'gen_rand_cls_combs' from data_manager
            cls_combs = gen_rand_cls_combs(labels)

            # In each epoch, we do a full pass over the triplets that can be generated from the class pairs
            epoch_batches = 0
            epoch_loss = 0
            # batch class pairs
            batches_cls_comb = range(0, len(cls_combs), self.train_params.batch_sz)
            nb_batches = len(batches_cls_comb)

            for batch_cls_comb in batches_cls_comb:
                batch_startt = time.time()
                batch_range_ids = range(batch_cls_comb,
                                        min(len(cls_combs), batch_cls_comb + self.train_params.batch_sz))
                # create triplets for current batch, 'gen_triplet_from_cls_combs' from data_manager
                batch_triplet_ids = gen_triplet_from_cls_combs(cls_combs[batch_range_ids[0]:batch_range_ids[-1]],
                                                               labels)
                if len(batch_triplet_ids) == 0:
                    print(baseprint + "INFO: Triplet generation did not produce valid triplets, skipping batch...")
                    continue

                # get unique triplets [no longer needed]
                triplet_ids = np.vstack({tuple(row) for row in batch_triplet_ids})
                random.shuffle(triplet_ids)

                # learn with all batch triplets
                for batch_triplet in range(0, triplet_ids.shape[0], self.train_params.batch_sz):
                    cur_triplets_ids = triplet_ids[batch_triplet:min(triplet_ids.shape[0],
                                                                     batch_triplet + self.train_params.batch_sz)]
                    # form input data
                    input_data = []
                    target_labels = []
                    for t_id in range(len(cur_triplets_ids)):
                        try:
                            # input are image filenames
                            if large_scale:
                                tmp_img_fns = [input[cur_triplets_ids[t_id][0]],
                                               input[cur_triplets_ids[t_id][1]],
                                               input[cur_triplets_ids[t_id][2]]]
                                imgs = self.prepare_imgfns_for_input(tmp_img_fns)
                                input_data.append(imgs[0])
                                input_data.append(imgs[1])
                                input_data.append(imgs[2])
                            # input are already images
                            else:
                                input_data.append(input[cur_triplets_ids[t_id][0]])
                                input_data.append(input[cur_triplets_ids[t_id][1]])
                                input_data.append(input[cur_triplets_ids[t_id][2]])
                            # labels for each sample in the triplets
                            target_labels.append(labels[cur_triplets_ids[t_id][0]])
                            target_labels.append(labels[cur_triplets_ids[t_id][1]])
                            target_labels.append(labels[cur_triplets_ids[t_id][2]])
                        except Exception as inst:
                            print(baseprint + "ERROR: for triplet #{}: {}. Error was {}.".format(t_id,
                                                                                                 cur_triplets_ids[t_id],
                                                                                                 inst))

                    # Loss computation may fail if another process has requested GPU memory since last batch...
                    loss = None
                    while not loss:

                        try:
                            loss = self.iter_funcs['train'](input_data, target_labels)
                        except Exception as inst:
                            print(baseprint + "ERROR: Could not compute loss. Error was {}.".format(inst))
                            time.sleep(10)
                    epoch_loss += loss
                    total_loss += loss
                    total_batches += 1
                    epoch_batches += 1

                    self.train_info.append((total_batches, lrate, loss))
                    print(baseprint + "INFO: Epoch {}/{}, batch {} took {:.3f}s.".format(epoch + 1,
                                                                                        self.train_params.num_epochs,
                                                                                        epoch_batches,
                                                                                        time.time() - batch_startt))
                    sys.stdout.flush()
            avg_loss = total_loss / total_batches
            e_loss = epoch_loss / max(1.0, epoch_batches)
            print(baseprint + "INFO: Epoch loss: {}, Total average loss: {}.".format(e_loss, avg_loss))
            self.log_train_info(self.train_params.train_info_log_fn)
            if np.mod(epoch, self.train_params.step_save) == 0:
                tmp_fn = self.train_params.model_fn_prefix + '_iter' + str(epoch) + '.pkl'
                self.save_model(tmp_fn)
            print(baseprint + "INFO: Completed epoch {}/{} in {:.3f}s".format(epoch + 1,
                                                                              self.train_params.num_epochs,
                                                                              time.time() - epoch_startt))
        if total_batches == 0:
            total_batches = 1
        # should we save here?
        return total_loss / total_batches

    # find nearest neighors and test accuracy
    def eval(self, gal_data, gal_labels, probe_data, probe_labels, input_type=InputDataFormat.IMG_DATA):
        # get output
        if input_type == InputDataFormat.IMG_DATA:
            gal_outputs = self.get_outputs(gal_data)
            probe_outputs = self.get_outputs(probe_data)
        if input_type == InputDataFormat.FILE:
            gal_outputs = self.get_outputs_from_files(gal_data)
            probe_outputs = self.get_outputs_from_files(probe_data)
        # do match
        dist_mat = comp_distmat(probe_outputs, gal_outputs, DistType.L2)
        evaluate('match results', dist_mat, gal_labels, probe_labels)
