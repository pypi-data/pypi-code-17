'''
deep model for matching images
use metric loss, e.g. triplet loss

'''

import time
import random

import theano
import theano.tensor as T

import lasagne
from lasagne.layers import InputLayer, DenseLayer, DropoutLayer
from lasagne.layers import NonlinearityLayer
from lasagne.layers import Conv2DLayer as ConvLayer
#from lasagne.layers.dnn import Conv2DDNNLayer as ConvLayer
from lasagne.layers import Pool2DLayer
from lasagne.layers import LocalResponseNormalization2DLayer as NormLayer
from lasagne.nonlinearities import softmax, sigmoid, identity

from common import LossType, TripletDist, TripletType, InputDataFormat
from base_model import ModelParamsBase, TrainParamsBase, BaseModel, ExptConfigBase
from data_manager import *
from search_tools import *


class TripletModelParams(ModelParamsBase):
    pass


class TripletLossTrainParams(TrainParamsBase):
    loss_type = LossType.Triplet
    triplet_margin = 1
    triplet_mode = TripletType.Random
    triplet_dist = TripletDist.L1
    num_triplets = 100
    extra_info = ''


class DeepMatcherExptConfig(ExptConfigBase):

    def fill_params(self):
        self.train_params.model_fn_prefix = \
            '../models/{}_matcher_{}_{}'.format(self.db_name, self.loss_name, self.extra_info)
        self.train_params.model_fn = self.train_params.model_fn_prefix + '.pkl'


# it is usually advised to train a classifier first as initialization and fine-tune a matcher
class DeepMatcher(BaseModel):

    def create_iter_train_func(self, lrate, th=0.5):
        if self.train_params.loss_type == LossType.Triplet or self.train_params.loss_type == LossType.TripletImproved:
            # output are stacked: repeating (anchor, positive, negative)
            output = lasagne.layers.get_output(self.net[self.model_params.output_layer_name])
            
            if hasattr(self.train_params, 'triplet_dist') and self.train_params.triplet_dist == TripletDist.L1:
                # l1
                print('Using L1 distance for triplets')
                #dist1 = (T.abs_(output[::3]-output[1::3])).sum(axis=1)/output.shape[1]
                #dist2 = (T.abs_(output[::3]-output[2::3])).sum(axis=1)/output.shape[1]
                dist1 = (T.abs_(output[::3]-output[1::3])).sum(axis=1)/T.shape(output)[1]
                dist2 = (T.abs_(output[::3]-output[2::3])).sum(axis=1)/T.shape(output)[1]
            else:
                # l2 normalization
                output  = output / output.norm(2, axis=1).reshape((output.shape[0],1))
                dist1 = ((output[::3]-output[1::3])**2).sum(axis=1)
                dist2 = ((output[::3]-output[2::3])**2).sum(axis=1)
                
            dist = dist1 - dist2 + self.train_params.triplet_margin
            samp_sgn = T.gt(dist, 0.0)
            train_loss = T.sum(dist * samp_sgn) / T.shape(output)[0]

            if self.train_params.loss_type == LossType.TripletImproved:
                print('Using triplet loss improved')
                # should we define an intra-class margin?
                dist_imp = dist1 - self.train_params.triplet_margin
                samp_sgn_imp = T.gt(dist_imp, 0.0)
                train_loss += T.sum(dist_imp * samp_sgn_imp)/T.shape(output)[0]

            # updates for training
            params = self.get_target_params(for_training=True)
            print('total trainable parameter number: {}'.format(lasagne.layers.count_params(self.net[self.model_params.output_layer_name])))
            print('params parameter number: {}'.format(len(params)))
            print('train with learning rate: {:.6f}'.format(lrate))
            if hasattr(self.train_params,'debug') and self.train_params.debug:
                theano.printing.pydotprint(train_loss, "loss.svg", format='svg')
                theano.printing.pydotprint(train_loss, "loss_compact.svg", format='svg', compact=True)
            updates = lasagne.updates.nesterov_momentum(train_loss, params, learning_rate=lrate, momentum=0.9)
            # functions
            start_comp = time.time()
            train_fn = theano.function(
                [self.net['input'].input_var], 
                train_loss, updates=updates)
            print "Train function compilation took:",str(time.time()-start_comp)+"s."
            return train_fn
        else:
            raise NotImplementedError('other matching loss is not implemented')


    def learn_model_large_scale_triplet_large_class_nb(self, train_img_fns, train_labels):
        ''' Train a model with triplet loss using image filenames as input.

        :param train_img_fns: list of all training images filenames
        :param train_labels: list of all training images labels
        :return:
        '''
        if 'train' not in self.iter_funcs:
            self.create_iter_funcs(self.train_params.lrate)
        lrate = self.train_params.lrate
        train_img_fns = np.asarray(train_img_fns)
        total_batches = 0
        total_loss = 0
        nb_samples = len(train_labels)
        out = lasagne.layers.get_output(self.net[self.model_params.output_layer_name])
        get_output = theano.function([self.net['input'].input_var], out)

        for epoch in range(self.train_params.num_epochs):
            epoch_startt = time.time()
            if np.mod(epoch, self.train_params.step_lr) == 0 and epoch > 0:
                lrate = self.train_params.gamma_lr * lrate
                print("Learning rate is now {}".format(lrate))
                self.create_iter_funcs(lrate)
            ids = range(nb_samples)
            np.random.shuffle(ids)
            img_fns = np.asarray([train_img_fns[id] for id in ids])
            labels = np.asarray([train_labels[id] for id in ids])
            # In each epoch, we do a full pass over the triplets that can be generated from the class pairs
            epoch_batches = 0
            epoch_loss = 0
            # we need to have a rather larger pool of samples to generate triplets
            batch_sample_size = self.train_params.batch_sz*16
            for batch_sample_start in range(0, nb_samples, batch_sample_size):
                # generate this batch class pairs
                batch_labels = labels[batch_sample_start:min(nb_samples,batch_sample_start+batch_sample_size)]
                batch_img_fns = img_fns[batch_sample_start:min(nb_samples,batch_sample_start+batch_sample_size)]
                cls_combs = gen_rand_cls_combs(batch_labels)
                batches_cls_comb = range(0, len(cls_combs), self.train_params.batch_sz*8)
                nb_batches = len(batches_cls_comb)
                for batch_cls_comb in batches_cls_comb:
                    batch_startt = time.time()
                    if self.train_params.triplet_mode == TripletType.Random:
                        #print 'running random triplets mode...'
                        batch_range_ids = range(batch_cls_comb, min(len(cls_combs), batch_cls_comb+self.train_params.batch_sz*8))
                        print "batch_range_ids length: {}".format(len(batch_range_ids))
                        # create triplets for current batch
                        batch_triplet_ids = gen_triplet_from_cls_combs(cls_combs[batch_range_ids[0]:batch_range_ids[-1]], batch_labels)
                        #print("Built {} triplets for batch {}".format(len(batch_triplet_ids), epoch_batches))
                        if len(batch_triplet_ids)==0:
                            print("Triplet generation did not produce valid triplets, skipping batch...")
                            continue
                        # get unique triplets [no longer needed]
                        triplet_ids = np.vstack({tuple(row) for row in batch_triplet_ids})
                        random.shuffle(triplet_ids)
                        # learn with all batch triplets
                        for batch_triplet in range(0, triplet_ids.shape[0], self.train_params.batch_sz):
                            cur_triplets_ids = triplet_ids[batch_triplet:min(triplet_ids.shape[0],
                                                                             batch_triplet+self.train_params.batch_sz)]
                            print "cur_triplets_ids.shape: {}".format(cur_triplets_ids.shape)
                            # form input data
                            input_data = []
                            for id in range(len(cur_triplets_ids)):
                                try:
                                    # sanity check
                                    ap_ok = batch_labels[cur_triplets_ids[id][0]] == batch_labels[cur_triplets_ids[id][1]]
                                    an_ok = batch_labels[cur_triplets_ids[id][0]] != batch_labels[cur_triplets_ids[id][2]]
                                    if not (ap_ok and an_ok):
                                        triplet_labels = (batch_labels[cur_triplets_ids[id][0]],
                                                          batch_labels[cur_triplets_ids[id][1]],
                                                          batch_labels[cur_triplets_ids[id][2]])
                                        print_inv = "Invalid triplet #{} generated {}, labels {}"
                                        raise ValueError(print_inv.format(id,
                                                                          cur_triplets_ids[id],
                                                                          triplet_labels))
                                    tmp_img_fns = [batch_img_fns[cur_triplets_ids[id][0]],
                                                   batch_img_fns[cur_triplets_ids[id][1]],
                                                   batch_img_fns[cur_triplets_ids[id][2]]]
                                    imgs = self.prepare_imgfns_for_input(tmp_img_fns)
                                    input_data.append(imgs[0])
                                    input_data.append(imgs[1])
                                    input_data.append(imgs[2])
                                except Exception as inst:
                                    print("[error for triplet #{}] {}".format(id, cur_triplets_ids[id]))
                                    print("Error was {}.".format(inst))
                            if not input_data:
                                print("skipping empty batch.")
                                continue
                            loss = None
                            if hasattr(self.train_params,'debug') and self.train_params.debug and total_batches % 1000 == 0:
                                output = get_output(input_data)
                                dist1 = (T.abs_(output[::3]-output[1::3])).sum(axis=1)/output.shape[1]
                                dist2 = (T.abs_(output[::3]-output[2::3])).sum(axis=1)/output.shape[1]
                                dist_imp = dist1 - self.train_params.triplet_margin
                                debug_print = "Batch #{} output shape is {}. dist1 {}, dist2 {}, dist_imp {}"
                                print(debug_print.format(nb_batches,
                                                         T.shape(output).eval(),
                                                         dist1.eval(),
                                                         dist2.eval(),
                                                         dist_imp.eval()))
                            while not loss:
                                try:
                                    loss = self.iter_funcs['train'](input_data)
                                except Exception as inst:
                                    print("[Error] Could not compute loss. Error was {}.".format(inst))
                                    time.sleep(10)
                            epoch_loss += loss
                            total_loss += loss
                            epoch_batches += 1
                            if batch_triplet > 1:
                                nb_batches += 1
                            total_batches += 1
                            
                    print("Epoch {}/{}, batch {} took {:.3f}s.".format(epoch+1, self.train_params.num_epochs,
                                                                epoch_batches, nb_batches, time.time() - batch_startt))
                    sys.stdout.flush()
                print("Epoch loss: {}\nTotal average loss: {}.".format(epoch_loss/max(1.0,epoch_batches),
                                                                total_loss/total_batches))

                if np.mod(epoch, self.train_params.step_save) == 0:
                    tmp_fn = self.train_params.model_fn_prefix + '_iter' + str(epoch) + '.pkl'
                    self.save_model(tmp_fn)
            print("Completed epoch {}/{} in {:.3f}s".format(epoch+1, self.train_params.num_epochs,
                                                             time.time() - epoch_startt))
        if total_batches == 0:
                total_batches = 1
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

    # All functions below are deprecated...

    # NOT TESTED
    # triplet_fns is a Nx3 array, each row is a triplet (anchor, positive, negative), each cell is a filename
    def learn_model_with_tripletfns(self, train_triplet_fns, num_epochs):
        if train_triplet_fns.shape[1] != 3:
            raise Exception('invalid triplet files for training, it has to be a Nx3 string matrix')

        if 'train' not in self.iter_funcs:
            self.create_iter_funcs(self.train_params.lrate)

        train_triplet_fns = np.asarray(train_triplet_fns)
        print 'training in normal mode'
        total_batches = 0
        total_loss = 0
        # We iterate over epochs:
        cls_combs = gen_cls_combs(train_labels)
        for epoch in range(self.train_params.num_epochs):  # this is a local epoch when training in large scale mode
            start_time = time.time()
            if np.mod(epoch, self.train_params.step_lr) == 0 and epoch > 0:
                lrate = self.train_params.gamma_lr * lrate
                print("Learning rate is now {}".format(lrate))
                self.create_iter_funcs(lrate)

            print 'running random triplets mode...'
            # load image and form triplet data
            # In each epoch, we do a full pass over the training data:
            train_loss = 0
            train_batches = 0
            # batch triplets
            for batch in range(0, train_triplet_fns.shape[0], self.train_params.batch_sz):
                batch_startt = time.time()
                cur_triplets_fns = train_triplet_fns[
                                   batch:min(triplet_ids.shape[0], batch + self.train_params.batch_sz)]
                print "cur_triplets.shape: {}".format(cur_triplets.shape)
                # form input data
                input_data = []
                for id in range(len(cur_triplets_fns)):
                    img_fns = [cur_triplets_fns[id][0], cur_triplets_fns[id][1], cur_triplets_fns[id][2]]
                    imgs = self.prepare_imgfns_for_input(img_fns)
                    input_data.append(imgs[0])
                    input_data.append(imgs[1])
                    input_data.append(imgs[2])
                loss = self.iter_funcs['train'](input_data)
                train_loss += loss
                total_loss += loss
                train_batches += 1
                total_batches += 1
                print("Epoch {}/{}, batch {} took {:.3f}s".format(
                    epoch + 1, self.train_params.num_epochs, train_batches,
                    time.time() - batch_startt))
                print("  training loss:\t\t{:.6f}".format(total_loss / total_batches))

        if total_batches == 0:
            total_batches = 1
        return total_loss / total_batches

    def learn_model_large_scale_triplet(self, train_img_fns, train_labels):
        ''' Train a model with triplet loss using image filenames as input.

        :param train_img_fns: list of all training images filenames
        :param train_labels: list of all training images labels
        :return:
        '''
        if 'train' not in self.iter_funcs:
            self.create_iter_funcs(self.train_params.lrate)
        lrate = self.train_params.lrate
        train_img_fns = np.asarray(train_img_fns)
        total_batches = 0
        total_loss = 0
        self.train_info
        for epoch in range(self.train_params.num_epochs):
            epoch_startt = time.time()
            if np.mod(epoch, self.train_params.step_lr) == 0 and epoch > 0:
                lrate = self.train_params.gamma_lr * lrate
                print("Learning rate is now {}".format(lrate))
                self.create_iter_funcs(lrate)

            ids = range(len(train_labels))
            np.random.shuffle(ids)
            img_fns = np.asarray([train_img_fns[id] for id in ids])
            labels = np.asarray([train_labels[id] for id in ids])
            # generate this epoch class pairs
            cls_combs = gen_rand_cls_combs(labels)  # in data_manager
            # In each epoch, we do a full pass over the triplets that can be generated from the class pairs
            epoch_batches = 0
            epoch_loss = 0
            # batch class pairs
            batches_cls_comb = range(0, len(cls_combs), self.train_params.batch_sz)
            nb_batches = len(batches_cls_comb)
            for batch_cls_comb in batches_cls_comb:
                batch_startt = time.time()
                if self.train_params.triplet_mode == TripletType.Random:
                    batch_range_ids = range(batch_cls_comb,
                                            min(len(cls_combs), batch_cls_comb + self.train_params.batch_sz))
                    # create triplets for current batch
                    batch_triplet_ids = gen_triplet_from_cls_combs(cls_combs[batch_range_ids[0]:batch_range_ids[-1]],
                                                                   labels)  # in data_manager
                    # print("Built {} triplets for batch {}".format(len(batch_triplet_ids), epoch_batches))
                    if len(batch_triplet_ids) == 0:
                        print("Triplet generation did not produce valid triplets, skipping batch...")
                        continue
                    # get unique triplets [no longer needed]
                    triplet_ids = np.vstack({tuple(row) for row in batch_triplet_ids})
                    random.shuffle(triplet_ids)
                    # learn with all batch triplets
                    for batch_triplet in range(0, triplet_ids.shape[0], self.train_params.batch_sz):
                        cur_triplets_ids = triplet_ids[batch_triplet:min(triplet_ids.shape[0],
                                                                         batch_triplet + self.train_params.batch_sz)]
                        # print "cur_triplets_ids.shape: {}".format(cur_triplets_ids.shape)
                        # form input data
                        input_data = []
                        for id in range(len(cur_triplets_ids)):
                            try:
                                tmp_img_fns = [img_fns[cur_triplets_ids[id][0]],
                                               img_fns[cur_triplets_ids[id][1]],
                                               img_fns[cur_triplets_ids[id][2]]]
                                imgs = self.prepare_imgfns_for_input(tmp_img_fns)
                                input_data.append(imgs[0])
                                input_data.append(imgs[1])
                                input_data.append(imgs[2])
                            except Exception as inst:
                                print("[Error for triplet #{}] {}".format(id, cur_triplets_ids[id]))
                                print("Error was {}.".format(inst))
                        # Loss computation may fail if another process has requested GPU memory since last batch...
                        loss = None
                        while not loss:
                            try:
                                loss = self.iter_funcs['train'](input_data)
                            except Exception as inst:
                                print("[Error] Could not compute loss. Error was {}.".format(inst))
                                sys.stdout.flush()
                                time.sleep(10)
                        epoch_loss += loss
                        total_loss += loss
                        epoch_batches += 1
                        if batch_triplet > 1:
                            nb_batches += 1
                        total_batches += 1
                        self.train_info.append((total_batches, lrate, loss))
                print("Epoch {}/{}, batch {}/{} took {:.3f}s.".format(epoch + 1, self.train_params.num_epochs,
                                                                      epoch_batches, nb_batches,
                                                                      time.time() - batch_startt))
                print("Epoch loss: {}\nTotal average loss: {}.".format(epoch_loss / max(1.0, epoch_batches),
                                                                       total_loss / total_batches))
                sys.stdout.flush()
                self.log_train_info(self.train_params.train_info_log_fn)
                if np.mod(epoch, self.train_params.step_save) == 0:
                    tmp_fn = self.train_params.model_fn_prefix + '_iter' + str(epoch) + '.pkl'
                    self.save_model(tmp_fn)
            print("Completed epoch {}/{} in {:.3f}s".format(epoch + 1, self.train_params.num_epochs,
                                                            time.time() - epoch_startt))
        if total_batches == 0:
            total_batches = 1
        return total_loss / total_batches

    def learn_model_large_scale_triplet_large_class_nb(self, train_img_fns, train_labels):
        ''' Train a model with triplet loss using image filenames as input.

        :param train_img_fns: list of all training images filenames
        :param train_labels: list of all training images labels
        :return:
        '''
        if 'train' not in self.iter_funcs:
            self.create_iter_funcs(self.train_params.lrate)
        lrate = self.train_params.lrate
        train_img_fns = np.asarray(train_img_fns)
        total_batches = 0
        total_loss = 0
        nb_samples = len(train_labels)
        self.train_info
        for epoch in range(self.train_params.num_epochs):
            epoch_startt = time.time()
            if np.mod(epoch, self.train_params.step_lr) == 0 and epoch > 0:
                lrate = self.train_params.gamma_lr * lrate
                print("Learning rate is now {}".format(lrate))
                self.create_iter_funcs(lrate)

            ids = range()
            np.random.shuffle(ids)
            img_fns = np.asarray([train_img_fns[id] for id in ids])
            labels = np.asarray([train_labels[id] for id in ids])
            # In each epoch, we do a full pass over the triplets that can be generated from the class pairs
            epoch_batches = 0
            epoch_loss = 0
            for batch_samples in range(0, nb_samples, self.train_params.batch_sz):
                # generate this batch class pairs
                batch_labels = labels[batch_samples]
                batch_img_fns = img_fns[batch_samples]
                cls_combs = gen_rand_cls_combs()
                batches_cls_comb = range(0, len(cls_combs), self.train_params.batch_sz)
                nb_batches = len(batches_cls_comb)
                for batch_cls_comb in batches_cls_comb:
                    batch_startt = time.time()
                    if self.train_params.triplet_mode == TripletType.Random:
                        print 'running random triplets mode...'
                        batch_range_ids = range(batch_cls_comb, min(len(cls_combs), batch_cls_comb+self.train_params.batch_sz))
                        # create triplets for current batch
                        batch_triplet_ids = gen_triplet_from_cls_combs(cls_combs[batch_range_ids[0]:batch_range_ids[-1]], batch_labels)
                        #print("Built {} triplets for batch {}".format(len(batch_triplet_ids), epoch_batches))
                        if len(batch_triplet_ids)==0:
                            print("Triplet generation did not produce valid triplets, skipping batch...")
                            continue
                        # get unique triplets [no longer needed]
                        triplet_ids = np.vstack({tuple(row) for row in batch_triplet_ids})
                        random.shuffle(triplet_ids)
                        # learn with all batch triplets
                        for batch_triplet in range(0, triplet_ids.shape[0], self.train_params.batch_sz):
                            cur_triplets_ids = triplet_ids[batch_triplet:min(triplet_ids.shape[0],
                                                                             batch_triplet+self.train_params.batch_sz)]
                            print "cur_triplets_ids.shape: {}".format(cur_triplets_ids.shape)
                            # form input data
                            input_data = []
                            for id in range(len(cur_triplets_ids)):
                                try:
                                    tmp_img_fns = [batch_img_fns[cur_triplets_ids[id][0]],
                                                   batch_img_fns[cur_triplets_ids[id][1]],
                                                   batch_img_fns[cur_triplets_ids[id][2]]]
                                    imgs = self.prepare_imgfns_for_input(tmp_img_fns)
                                    input_data.append(imgs[0])
                                    input_data.append(imgs[1])
                                    input_data.append(imgs[2])
                                except Exception as inst:
                                    print("[error for triplet #{}] {}".format(id, cur_triplets_ids[id]))
                                    print("Error was {}.".format(inst))
                            loss = self.iter_funcs['train'](input_data)
                            epoch_loss += loss
                            total_loss += loss
                            epoch_batches += 1
                            if batch_triplet > 1:
                                nb_batches += 1
                            total_batches += 1
                            self.train_info.append((total_batches, lrate, loss))
                print("Epoch {}/{}, batch {}/{} took {:.3f}s.".format(epoch+1, self.train_params.num_epochs,
                                                                epoch_batches, nb_batches, time.time() - batch_startt))
                print("Epoch loss: {}\nTotal average loss: {}.".format(epoch_loss/max(1.0,epoch_batches),
                                                                total_loss/total_batches))
                self.log_train_info(self.train_params.train_info_log_fn)
                if np.mod(epoch, self.train_params.step_save) == 0:
                    tmp_fn = self.train_params.model_fn_prefix + '_iter' + str(epoch) + '.pkl'
                    self.save_model(tmp_fn)
            print("Completed epoch {}/{} in {:.3f}s".format(epoch+1, self.train_params.num_epochs,
                                                             time.time() - epoch_startt))
        if total_batches == 0:
                total_batches = 1
        return total_loss / total_batches

    def learn_model(self, train_data, train_labels, val_data, val_labels, num_epochs):
        ## Only for hard triplets?
        # outputs = lasagne.layers.get_output(self.net['output']) # output or output_layer_name?
        # output_fn = theano.function([self.net['input'].input_var], outputs)
        # launch the training loop
        # mode = 1 # 0: random triplets; 1: hard triplets
        if 'train' not in self.iter_funcs:
            self.create_iter_funcs(self.train_params.lrate)

        print 'training in normal mode'
        total_batches = 0
        total_loss = 0
        # We iterate over epochs:
        cls_combs = gen_cls_combs(train_labels)
        for epoch in range(self.train_params.num_epochs):  # this is a local epoch when training in large scale mode
            start_time = time.time()
            ''' generate meaningful triplets
                idea1: 1) must cover each identity in each iteration
                        2) each batch selects a subset of identity and a subset of samples within each identity
                        3) triplets are selected from the subset of samples
                idea2: 1) must cover each sample (as anchor) in each iteration
                        2) each batch selects a subset of samples as anchor points
                        3) triplets are selected from the subset of samples
            '''
            if np.mod(epoch, self.train_params.step_lr) == 0 and epoch > 0:
                lrate = self.train_params.gamma_lr * lrate
                print("Learning rate is now {}".format(lrate))
                self.create_iter_funcs(lrate)

            if self.train_params.triplet_mode == TripletType.Random:
                print 'running random triplets mode...'
                # create triplets for current epoch
                all_triplet_ids = gen_random_triplets(train_labels, self.train_params.num_triplets)
                print "all_triplet_ids.shape", all_triplet_ids.shape
                if all_triplet_ids.shape[0] == 0:
                    print "Triplet generation did not produce valid triplets, skipping epoch"
                    continue
                # get unique triplets
                triplet_ids = np.vstack({tuple(row) for row in all_triplet_ids})
                print "triplet_ids.shape", triplet_ids.shape
                random.shuffle(triplet_ids)
                # In each epoch, we do a full pass over the training data:
                train_loss = 0
                train_batches = 0
                # batch triplets
                for batch in range(0, triplet_ids.shape[0], self.train_params.batch_sz):
                    batch_startt = time.time()
                    cur_triplets = triplet_ids[batch:min(triplet_ids.shape[0], batch + self.train_params.batch_sz)]
                    print "cur_triplets.shape", cur_triplets.shape
                    # form input data
                    input_data = []
                    for id in range(len(cur_triplets)):
                        input_data.append(train_data[cur_triplets[id, 0]])
                        input_data.append(train_data[cur_triplets[id, 1]])
                        input_data.append(train_data[cur_triplets[id, 2]])
                    # input_data = np.empty((cur_triplets.shape[0]*3, train_data.shape[1], train_data.shape[2], train_data.shape[3]), dtype=theano.config.floatX)
                    # input_data[::3] = train_data[cur_triplets[:,0]]
                    # input_data[1::3] = train_data[cur_triplets[:,1]]
                    # input_data[2::3] = train_data[cur_triplets[:,2]]
                    loss = self.iter_funcs['train'](input_data)
                    train_loss += loss
                    total_loss += loss
                    train_batches += 1
                    total_batches += 1
                    print("Epoch {}/{}, batch {} took {:.3f}s".format(
                        epoch + 1, self.train_params.num_epochs, train_batches,
                        time.time() - batch_startt))
                    print("  training loss:\t\t{:.6f}".format(total_loss / total_batches))
            else:
                print 'running hard triplets mode...'
                # each comb defines a triplet space
                random.shuffle(cls_combs)
                train_loss = 0
                train_batches = 0
                batch_step = 3
                for batch in np.arange(0, len(cls_combs), step=batch_step):
                    batch_startt = time.time()
                    # select identities for current batch
                    cur_cls_combs = cls_combs[batch:batch + batch_step]
                    triplets = np.asarray([])
                    for comb in cur_cls_combs:
                        # sample images for class combs
                        cls_samps = gen_samps_from_cls(train_labels, comb, 10)
                        cur_sel_samps = cls_samps[0] + cls_samps[1]
                        # find hard triplets
                        outputs = output_fn(train_data[cur_sel_samps])
                        cur_labels = train_labels[cur_sel_samps]
                        cur_triplets = gen_hard_triplets(outputs, cur_labels, batch_size * 2)
                        # update to global ids
                        cur_triplets[:, 0] = np.asarray(cur_sel_samps)[cur_triplets[:, 0]]
                        cur_triplets[:, 1] = np.asarray(cur_sel_samps)[cur_triplets[:, 1]]
                        cur_triplets[:, 2] = np.asarray(cur_sel_samps)[cur_triplets[:, 2]]
                        if triplets.size == 0:
                            triplets = cur_triplets
                        else:
                            triplets = np.vstack((triplets, cur_triplets))

                    print triplets.shape
                    for sel_triplets_ind in np.arange(0, len(triplets), step=batch_size):
                        sel_triplets = triplets[sel_triplets_ind:sel_triplets_ind + batch_size]
                        print sel_triplets.shape
                        # veritify triplet correctness
                        for triplet in sel_triplets:
                            assert train_labels[triplet[0]] == train_labels[triplet[1]] and train_labels[triplet[0]] != \
                                                                                            train_labels[triplet[2]]
                        # form input data
                        input_data = np.empty(
                            (batch_size * 3, train_data.shape[1], train_data.shape[2], train_data.shape[3]),
                            dtype=theano.config.floatX)
                        input_data[::3] = train_data[sel_triplets[:, 0]]
                        input_data[1::3] = train_data[sel_triplets[:, 1]]
                        input_data[2::3] = train_data[sel_triplets[:, 2]]
                        if self.loss_type == LossType.TripletClassification:
                            train_targets = np.empty((batch_size * 3), dtype=np.int32)
                            train_targets[::3] = train_labels[sel_triplets[:, 0]]
                            train_targets[1::3] = train_labels[sel_triplets[:, 1]]
                            train_targets[2::3] = train_labels[sel_triplets[:, 2]]
                            loss = self.iter_funcs['train'](input_data, train_targets)
                        else:
                            loss = self.iter_funcs['train'](input_data)
                        # print('useful triplets ratio: {}'.format(useful_num/batch_size))
                        train_loss += loss
                        total_loss += loss
                        train_batches += 1
                        total_batches += 1
                        print("Epoch {}/{}, batch {} took {:.3f}s".format(
                            epoch + 1, num_epochs, train_batches,
                            time.time() - batch_startt))
                        print("  training loss:\t\t{:.6f}".format(train_loss / train_batches))
            if np.mod(epoch, self.train_params.step_save) == 0 and epoch > 0:
                self.save_model(self.train_params.model_fn_prefix + "_epoch" + str(epoch) + ".pkl")
            print("Epoch {}/{} took {:.3f}s".format(epoch + 1, self.train_params.num_epochs, time.time() - start_time))
        if total_batches == 0:
            total_batches = 1
        return total_loss / total_batches

