''' 
definition of basic things for deep model learning 

'''

import sys
import os
import gzip
import cPickle as pickle
from sets import Set
import random
import numpy as np
import time
import matplotlib.pyplot as plt
import logging

import theano
import theano.tensor as T
#import theano.compile.nanguardmode
import lasagne
from lasagne.layers import InputLayer, DenseLayer, DropoutLayer
#from lasagne.layers import NonlinearityLayer
from lasagne.layers import Conv2DLayer as ConvLayer
#from lasagne.layers.dnn import Conv2DDNNLayer as ConvLayer
from lasagne.layers import MaxPool2DLayer as PoolLayer
from lasagne.layers import LocalResponseNormalization2DLayer as NormLayer
from lasagne.nonlinearities import softmax

from ModelTools import *
from ModelFactory import ModelType, ModelFactory
from DataManager import *


class LossType:
    Classification = 0
    Triplet = 1
    TripletClassification = 2
    PairClassification = 3



''' params to define the model '''
class DeepModelParamsBase():
    model_name = ''
    model_type = ModelType.IMAGENET_GNET
    img_sz = (224,224)
    # classification class number
    cls_num = 10
    # layer for extract output, e.g. feature, prediction etc
    output_layer_name = 'output'
    flip_image = False
    crops_image = False
    crops_image_nb = 0


''' params for training a model '''
class DeepModelTrainParamsBase():
    loss_type = LossType.Classification
    triplet_margin = 1
    triplet_mode = TripletType.Random
    # initial learning rate
    lrate = 0.1
    # num of batches to reduce learning rate
    step_lr = 10000
    # learning rate decay coeff
    gamma_lr = 0.5
    # step/epoch to save model
    step_save = 100
    num_epochs = 10
    # prefix
    model_fn_prefix = ''
    model_fn = ''
    batch_sz = 32
    # training data related
    extra_input_info = {}
    # layers to extract parameters
    # if 'OUTPUT' is used, all parameters under output layer will be extracted
    param_layer_names = ['OUTPUT']


    

# base model (CNN classifier) to be derived to create custom deep model
class BaseDeepModel(object):

    ''' data '''
    net = {}
    class_names = []    # label name
    mean_img = None
    # main parameters
    model_params = DeepModelParamsBase()
    train_params = DeepModelTrainParamsBase()
    iter_funcs = {}
    output_func = None
    ''' 
    training info for vis and logging
    each timestamp contains (iter id, train loss, learning rate etc)
    add it during training
    '''
    train_info = []

    def __init__(self, model_params_, train_params_):
        self.model_params = model_params_
        self.train_params = train_params_
        
    ''' data prepartion '''
    # input NXHXWXC format, modify and output NXCXHXW to feed in network
    def prepare_imgs_for_input(self, cv_imgs):
        return cvimg_to_cnn(cv_imgs)

    # form training data from image files w extra meta info
    def prepare_imgfns_for_input(self, img_fns, extra_info = None):
        cv_imgs = load_cv_imgs(img_fns, self.model_params.img_sz)
        return self.prepare_imgs_for_input(cv_imgs)

    ''' model definition '''
    # build custom model
    def build_model(self):
        self.net = {}

    # [OBSOLETE] called after build the pretrained model and load parameters
    def build_finetune_model(self):
        pass

    def load_caffe_weights(self,caffe_model_prototxt,caffe_model_path):
        self.net = fill_net_from_caffe_protxt(caffe_model_prototxt,caffe_model_path,self.net)
    
    ''' model training '''
    # divide data into batches
    def iterate_minibatches(self, inputs, targets, batchsize, shuffle=False):
        assert len(inputs) == len(targets)
        if shuffle:
            indices = np.arange(len(inputs))
            np.random.shuffle(indices)
        for start_idx in range(0, len(inputs) - batchsize + 1, batchsize):
            if shuffle:
                excerpt = indices[start_idx:start_idx + batchsize]
            else:
                excerpt = slice(start_idx, start_idx + batchsize)
            yield inputs[excerpt], targets[excerpt]
       
    # extract target params for training / testing / saving
    def get_target_params(self, for_training=True):
        params = []
        for layer_name in self.train_params.param_layer_names:
            if layer_name == 'OUTPUT':
                params = lasagne.layers.get_all_params(self.net[self.model_params.output_layer_name], trainable=for_training)
                break
            else:
                params.append(self.net[layer_name].W)
                params.append(self.net[layer_name].b)
        return params

    def get_target_param_vals(self):
        param_vals = []
        for layer_name in self.train_params.param_layer_names:
            if layer_name == 'OUTPUT':
                param_vals = lasagne.layers.get_all_param_values(self.net[self.model_params.output_layer_name])
                break
            else:
                param_vals.append(self.net[layer_name].W.get_value())
                param_vals.append(self.net[layer_name].b.get_value())
        return param_vals

    def set_target_params(self, param_vals):
        assert len(self.train_params.param_layer_names) > 0, 'no parameter layer is specified, set params like this will have random values'
        for i in range(len(self.train_params.param_layer_names)):
            if self.train_params.param_layer_names[i] == 'OUTPUT' or (len(self.train_params.param_layer_names)==1 and len(param_vals)>2):
                lasagne.layers.set_all_param_values(self.net[self.model_params.output_layer_name], param_vals)
                break
            else:
                self.net[self.train_params.param_layer_names[i]].W.set_value(param_vals[2*i])
                self.net[self.train_params.param_layer_names[i]].b.set_value(param_vals[2*i+1])

    # call explicitly before train
    def create_iter_funcs(self, lrate):
        self.iter_funcs['train'] = self.create_iter_train_func(lrate)
        self.iter_funcs['eval'] = self.create_iter_eval_func()

    # define training function
    def create_iter_train_func(self, lrate, th=0.5):
        if self.train_params.loss_type == LossType.Classification:
            # compute classification loss
            target_var = T.ivector('train_targets')
            # shouldn't we use self.model_params.output_layer_name?
            train_output = lasagne.layers.get_output(self.net['output'])
            train_loss = lasagne.objectives.categorical_crossentropy(train_output, target_var)
            train_loss = train_loss.mean()
            # updates for training
            params = self.get_target_params(for_training=True)
            print 'total trainable parameter variable number: {}'.format(len(params))
            print 'train with learning rate: {:.6f}'.format(lrate)
            updates = lasagne.updates.nesterov_momentum(train_loss, params, learning_rate=lrate, momentum=0.9)
            # functions
            start_comp = time.time()
            train_fn = theano.function(
                [self.net['input'].input_var, target_var], 
                train_loss, updates=updates)
            print "Train function compilation took:",str(time.time()-start_comp)+"s."
        if self.train_params.loss_type == LossType.Triplet:
            # TODO: move customized code to a subclass instead of in the base class
            # if input is all datal plus ids
            #triplet_ids = T.imatrix("triplet_ids") 
            #dist1 = ((output[triplet_ids[:,0]]-output[triplet_ids[:,1]])**2).sum(axis=1)
            #dist2 = ((output[triplet_ids[:,0]]-output[triplet_ids[:,2]])**2).sum(axis=1)
            # output are stacked: repeating (anchor, similar, dissimilar)
            # use self.model_params.output_layer_name?
            #output = lasagne.layers.get_output(self.net['output'])
            output = lasagne.layers.get_output(self.net[self.model_params.output_layer_name])
            if hasattr(self.train_params, 'triplet_dist') and self.train_params.triplet_dist==TripletDist.Hamming:
                # L1 norm
                dist1 = (abs(output[::3]-output[1::3])).sum(axis=1)
                dist2 = (abs(output[::3]-output[2::3])).sum(axis=1)
            else:
                # l2 norm
                dist1 = ((output[::3]-output[1::3])**2).sum(axis=1)
                dist2 = ((output[::3]-output[2::3])**2).sum(axis=1)
            dist = dist1 - dist2 + self.train_params.triplet_margin
            samp_sgn = T.gt(dist, 0.0)
            train_loss = T.sum(dist * samp_sgn)/T.shape(output)[0]*3
            # compute percentage of triplet with loss 0
            useful_num = samp_sgn.sum()
            # updates for training
            #params = lasagne.layers.get_all_params(self.net['output'], trainable=True)
            params = self.get_target_params(for_training=True)
            #print('total trainable parameter number: {}'.format(lasagne.layers.count_params(self.net['output'])))
            print('total trainable parameter number: {}'.format(lasagne.layers.count_params(self.net[self.model_params.output_layer_name])))
            print('params parameter number: {}'.format(len(params)))
            print('train with learning rate: {:.6f}'.format(lrate))
            updates = lasagne.updates.nesterov_momentum(train_loss, params, learning_rate=lrate, momentum=0.9)
            # functions
            start_comp = time.time()
            train_fn = theano.function(
                [self.net['input'].input_var], 
                train_loss, updates=updates)
            print "Train function compilation took:",str(time.time()-start_comp)+"s."
        
        return train_fn

    # define testing function
    def create_iter_eval_func(self):
        target_var = T.ivector('eval_targets')
        eval_output = lasagne.layers.get_output(self.net['output'])
        eval_loss = lasagne.objectives.categorical_crossentropy(eval_output, target_var)
        eval_loss = eval_loss.mean()
        pred = T.argmax(eval_output, axis=1)
        accuracy = T.mean(T.eq(pred, target_var), dtype=theano.config.floatX)
        eval_fn = theano.function(
            [self.net['input'].input_var, target_var],
            [eval_loss, accuracy])
        return eval_fn

    def learn_triplet_loss(self, train_data, train_labels, num_epochs):
        ## Only for hard triplets?
        #outputs = lasagne.layers.get_output(self.net['output']) # output or output_layer_name?
        #output_fn = theano.function([self.net['input'].input_var], outputs)
        # launch the training loop
        #mode = 1 # 0: random triplets; 1: hard triplets
        print("Starting training...")
        total_batches = 0
        total_loss = 0
        # We iterate over epochs:
        cls_combs = gen_cls_combs(train_labels)
        for epoch in range(self.train_params.num_epochs): # this is a local epoch when training in large scale mode
            start_time = time.time()
            ''' generate meaningful triplets
                idea1: 1) must cover each identity in each iteration
                        2) each batch selects a subset of identity and a subset of samples within each identity
                        3) triplets are selected from the subset of samples
                idea2: 1) must cover each sample (as anchor) in each iteration
                        2) each batch selects a subset of samples as anchor points
                        3) triplets are selected from the subset of samples
            '''
            if np.mod(epoch, self.train_params.step_lr)==0 and epoch>0:
                lrate=self.train_params.gamma_lr*lrate
                print("Learning rate is now {}".format(lrate))
                self.create_iter_funcs(lrate)

            if self.train_params.triplet_mode == TripletType.Random:
                print 'running random triplets mode...'
                # create triplets for current epoch
                all_triplet_ids = gen_random_triplets(train_labels, self.train_params.nb_triplets)
                print "all_triplet_ids.shape",all_triplet_ids.shape
                if all_triplet_ids.shape[0]==0:
                    print "Triplet generation did not produce valid triplets, skipping epoch"
                    continue
                # get unique triplets
                triplet_ids = np.vstack({tuple(row) for row in all_triplet_ids})
                print "triplet_ids.shape",triplet_ids.shape
                random.shuffle(triplet_ids)
                # In each epoch, we do a full pass over the training data:
                train_loss = 0
                train_batches = 0
                # batch triplets
                for batch in range(0, triplet_ids.shape[0], self.train_params.batch_sz):
                    batch_startt = time.time()
                    cur_triplets = triplet_ids[batch:min(triplet_ids.shape[0],batch+self.train_params.batch_sz)]
                    print "cur_triplets.shape",cur_triplets.shape
                    # form input data
                    input_data = []
                    for id in range(len(cur_triplets)):
                        input_data.append(train_data[cur_triplets[id,0]])
                        input_data.append(train_data[cur_triplets[id,1]])
                        input_data.append(train_data[cur_triplets[id,2]])
                    #input_data = np.empty((cur_triplets.shape[0]*3, train_data.shape[1], train_data.shape[2], train_data.shape[3]), dtype=theano.config.floatX)
                    #input_data[::3] = train_data[cur_triplets[:,0]]
                    #input_data[1::3] = train_data[cur_triplets[:,1]]
                    #input_data[2::3] = train_data[cur_triplets[:,2]]
                    loss = self.iter_funcs['train'](input_data)
                    train_loss += loss
                    total_loss += loss
                    train_batches += 1
                    total_batches += 1
                    print("Epoch {}/{}, batch {} took {:.3f}s".format(
                        epoch+1, self.train_params.num_epochs, train_batches, 
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
                    cur_cls_combs = cls_combs[batch:batch+batch_step]
                    triplets = np.asarray([])
                    for comb in cur_cls_combs:
                        # sample images for class combs
                        cls_samps = gen_samps_from_cls(train_labels, comb, 10)
                        cur_sel_samps = cls_samps[0] + cls_samps[1]
                        # find hard triplets
                        outputs = output_fn(train_data[cur_sel_samps])
                        cur_labels = train_labels[cur_sel_samps]
                        cur_triplets = gen_hard_triplets(outputs, cur_labels, batch_size*2)
                        # update to global ids
                        cur_triplets[:,0] = np.asarray(cur_sel_samps)[cur_triplets[:,0]]
                        cur_triplets[:,1] = np.asarray(cur_sel_samps)[cur_triplets[:,1]]
                        cur_triplets[:,2] = np.asarray(cur_sel_samps)[cur_triplets[:,2]]
                        if triplets.size == 0:
                            triplets = cur_triplets
                        else:
                            triplets = np.vstack((triplets, cur_triplets))
                    
                    print triplets.shape
                    for sel_triplets_ind in np.arange(0, len(triplets), step=batch_size):
                        sel_triplets = triplets[sel_triplets_ind:sel_triplets_ind+batch_size]
                        print sel_triplets.shape
                        # veritify triplet correctness
                        for triplet in sel_triplets:
                            assert train_labels[triplet[0]] == train_labels[triplet[1]] and train_labels[triplet[0]] != train_labels[triplet[2]]
                        # form input data
                        input_data = np.empty((batch_size*3, train_data.shape[1], train_data.shape[2], train_data.shape[3]), dtype=theano.config.floatX)
                        input_data[::3] = train_data[sel_triplets[:,0]]
                        input_data[1::3] = train_data[sel_triplets[:,1]]
                        input_data[2::3] = train_data[sel_triplets[:,2]]
                        if self.loss_type == LossType.TripletClassification:
                            train_targets = np.empty((batch_size*3), dtype=np.int32)
                            train_targets[::3] = train_labels[sel_triplets[:,0]]
                            train_targets[1::3] = train_labels[sel_triplets[:,1]]
                            train_targets[2::3] = train_labels[sel_triplets[:,2]]
                            loss = self.iter_funcs['train'](input_data,train_targets)
                        else:
                            loss = self.iter_funcs['train'](input_data)
                        #print('useful triplets ratio: {}'.format(useful_num/batch_size))
                        train_loss += loss
                        total_loss += loss
                        train_batches += 1
                        total_batches += 1
                        print("Epoch {}/{}, batch {} took {:.3f}s".format(
                            epoch+1, num_epochs, train_batches,
                            time.time() - batch_startt))
                        print("  training loss:\t\t{:.6f}".format(train_loss / train_batches))
            if np.mod(epoch, self.train_params.step_save)==0 and epoch>0:
                self.save_model(self.train_params.model_fn_prefix+"_epoch"+str(epoch)+".pkl")
            print("Epoch {}/{} took {:.3f}s".format(epoch+1, self.train_params.num_epochs, time.time() - start_time))
        if total_batches==0:
            total_batches=1
        return total_loss / total_batches

    # use pairs to train classifier
    def learn_pairwise_loss(self, train_data, train_labels, num_epochs):
        pass

    def learn_clf_loss(self, train_data, train_labels, val_data, val_labels, num_epochs):
        train_data = np.asarray(train_data, np.float32)
        train_labels = np.asarray(train_labels, np.int32)
        # launch the training loop
        print("Starting training...")
        print('batch size: {}, epochs: {}'.format(self.train_params.batch_sz, num_epochs))
        total_batches = 0
        total_loss = 0
        # We iterate over epochs:
        for epoch in range(num_epochs):
            # In each epoch, we do a full pass over the training data:
            train_loss = 0
            train_batches = 0
            if np.mod(epoch,self.train_params.step_lr)==0 and epoch > 0:
                self.train_params.lrate *= self.train_params.gamma_lr
                print("Learning rate is now {}".format(self.train_params.lrate))
                self.create_iter_funcs(self.train_params.lrate)
                
            for batch in self.iterate_minibatches(train_data, train_labels, self.train_params.batch_sz):
                train_batch_startt = time.time()
                inputs, targets = batch
                loss = self.iter_funcs['train'](inputs, targets)
                train_loss += loss
                total_loss += loss
                train_batches += 1
                total_batches += 1
                print "Epoch {}/{}, batch {} took {:.3f}s".format(
                    epoch+1, num_epochs, train_batches, time.time() - train_batch_startt)
                print "  training loss:\t\t{:.6f}".format(total_loss / total_batches)
                # add code to change learning rate by recreate training function

                #if train_batches % 200 == 0:
                #    # validate after each batch training
                #    val_loss = 0
                #    val_batches = 0
                #    val_accu = 0
                #    val_startt = time.time()
                #    if val_data is None:
                #        print 'using train data for validation'
                #        val_data = train_data
                #        val_labels = train_labels
                #    for batch in self.iterate_minibatches(val_data, val_labels, self.train_params.batch_sz):
                #        inputs, targets = batch
                #        loss, accu = self.iter_funcs['eval'](inputs, targets)
                #        val_loss += loss
                #        val_accu += accu
                #        val_batches += 1
                #    print("Eval took {:.3f}s".format(time.time() - val_startt))
                #    print("  val loss:\t\t{:.6f}; val accu:\t\t{:.6f}".format(val_loss / val_batches, val_accu / val_batches))
            if np.mod(epoch, self.train_params.step_save)==0 and epoch>0:
                self.save_model(self.train_params.model_fn_prefix+"_epoch"+str(epoch)+".pkl")
        print('total batches: {}'.format(total_batches))
        return total_loss / total_batches

    # train from stratch or fine-tune, return average batch loss
    def learn_model(self, train_data, train_labels, val_data, val_labels, num_epochs):
        print 'training in normal mode'
        if 'train' not in self.iter_funcs:
            self.create_iter_funcs(self.train_params.lrate)
        if self.train_params.loss_type == LossType.Classification:
            return self.learn_clf_loss(train_data, train_labels, val_data, val_labels, num_epochs)
        if self.train_params.loss_type == LossType.Triplet or self.train_params.loss_type == LossType.TripletClassification:
            return self.learn_triplet_loss(train_data, train_labels, num_epochs)

    #　train on large scale data, load by batch
    def learn_model_large_scale(self, train_img_fns, train_labels, val_img_fns, val_labels):
        # val_img_fns, val_labels are not used?
        train_img_fns = np.asarray(train_img_fns)
        train_labels = np.asarray(train_labels)
        print 'training in large scale mode'
        self.create_iter_funcs(self.train_params.lrate)
        train_loss = 0
        train_batches = 0
        # confusion between large scale epoch and "local" epochs
        self.train_params.num_epochs_large_scale = self.train_params.num_epochs
        self.train_params.num_epochs = 1
        for epoch in range(self.train_params.num_epochs_large_scale):
            batch_num = 0
            # randomize
            ids = range(len(train_labels))
            np.random.shuffle(ids)
            img_fns = train_img_fns[ids]
            labels = train_labels[ids]
            #img_fns = [train_img_fns[id] for id in ids]
            #labels = [train_labels[id] for id in ids]
            # For triplet loss it would be better to have a different batch_sz at this point,
            # bigger than the actual batch size used for training.
            # This would help creating more meaningful triplets...
            for id in range(0, len(img_fns)-self.train_params.batch_sz, self.train_params.batch_sz):
                train_batches += 1
                batch_num += 1
                print('processing epoch {} batch {}'.format(epoch, batch_num))
                train_batch_startt = time.time()
                # decrease learning rate after certain iters
                if train_batches % self.train_params.step_lr == 0 and self.train_params.lrate >= 0.0001:
                    self.train_params.lrate *= self.train_params.gamma_lr
                    self.create_iter_funcs(self.train_params.lrate)
                
                batch_data_prepare_start = time.time()
                cur_batch_fns = img_fns[id:id+self.train_params.batch_sz]
                cur_batch_labels = labels[id:id+self.train_params.batch_sz]
                #print len(cur_batch_fns)
                imgs = self.prepare_imgfns_for_input(cur_batch_fns, self.train_params.extra_input_info)
                if imgs.shape[0] != cur_batch_labels.size:
                    print 'sample and label number not consistent, skip this batch'
                    continue
                print("batch data prepare time: {:.3f}s".format(time.time() - batch_data_prepare_start))
                #print imgs.shape
                #print cur_batch_labels.shape
                train_loss += self.learn_model(imgs, cur_batch_labels, None, None, 1)
                print("total batch time: {:.3f}s".format(time.time() - train_batch_startt))
                print 'epoch {}, batch {} loss: \t\t{:.8f}'.format(epoch+1, train_batches, train_loss / train_batches)
            
            if np.mod(epoch, self.train_params.step_save)==0:
                tmp_fn = self.train_params.model_fn_prefix + '_iter' + str(train_batches) + '.pkl'
                self.save_model(tmp_fn)

    ''' model testing '''
    # predict top K image labels
    def predict_img(self, img_fn, topK):
        print('testing image: ' + img_fn)
        # read image
        img_fns = [img_fn]
        input = self.prepare_imgfns_for_input(img_fns)
        # predict
        start = time.time()
        # np.array(lasagne.layers.get_output(self.net['output'], input, deterministic=True).eval())
        prob = self.get_outputs(input)
        print 'prediction time (without compilation): {}s'.format(time.time()-start)
        top_num = min(topK, len(prob[0]))
        top_labels = np.argsort(prob[0])[-1:-1-top_num:-1]
        top_prob = np.sort(prob[0])[-1:-1-top_num:-1]
        # show results
        for n, label in enumerate(top_labels):
            print('{}. {}: {}'.format(n+1, self.class_names[label], top_prob[n]))

    def create_output_func(self, flattern=True):
        if flattern:
            final_layer = lasagne.layers.FlattenLayer(self.net[self.model_params.output_layer_name])
        else:
            final_layer = self.net[self.model_params.output_layer_name]
        output = lasagne.layers.get_output(final_layer, deterministic=True)
        startt = time.time()
        self.output_func = theano.function([self.net['input'].input_var], output)
        print 'output function built. time cost: {}'.format(time.time()-startt)

    def get_outputs_from_files(self, input_fns, batch_size=-1, flattern=True):
        input_data = self.prepare_imgfns_for_input(input_fns)
        return self.get_outputs(input_data, batch_size, flattern)

    def get_outputs(self, input_data, batch_sz=-1, flattern=True):
        # ensure all feature is 1d
        if self.output_func is None:
            self.create_output_func(flattern)

        all_feats = None
        startt = time.time()
        if batch_sz == -1:
            all_feats = self.output_func(input_data)
        else:
            for i in np.arange(0, input_data.shape[0], batch_sz):
                cur_feat = self.output_func(input_data[i:i+batch_sz])
                if all_feats is None:
                    all_feats = cur_feat
                else:
                    all_feats = np.vstack((all_feats, cur_feat))
                print '{}/{}'.format(len(all_feats), len(input_data))
        
        print 'compute outputs for {}, time cost: {}'.format(len(input_data), time.time()-startt)
        return all_feats

    def eval_clf(self, test_data, test_labels):
        eval_fn = self.create_iter_eval_func()
        loss, accu = eval_fn(test_data, test_labels)
        print('classification accuracy: {:.6f}'.format(accu))

    ''' model I/O '''
    def save_model(self, save_fn):
        #params = self.get_target_param_vals()
        # should we always use that instead?
        params = lasagne.layers.get_all_param_values(self.net[self.model_params.output_layer_name])
        data = {}
        data['param_vals'] = params
        data['class_names'] = self.class_names
        data['mean_img'] = self.mean_img
        with open(save_fn, 'wb') as f:
            pickle.dump(data, f)
        print('saved model to {}'.format(save_fn))

    # with default name for corresponding data
    def load_model(self, save_fn, key_names = {'class_names': "class_names", "mean_img": "mean_img", "param_vals": "param_vals"}):
        print 'loading model from {}'.format(save_fn)
        startt = time.time()
        data = pickle.load(open(save_fn, 'rb'))
        params = data[key_names['param_vals']]
        # cast to standard type
        for i in range(len(params)):
            params[i] = params[i].astype(np.float32)
        self.class_names = data[key_names['class_names']]
        self.mean_img = data[key_names['mean_img']]
        #try:
        self.set_target_params(params)
        print('model loaded from {}, time cost: {}'.format(save_fn, time.time()-startt))
        #except:
        #    print "Could not run set_target_params."


    ''' model utilities '''
    def draw_train_info(self, to_save=False, save_fn='training_loss.png'):
        '''
        plot training loss at current point
        '''
        plt.title('training loss')
        plt.grid()
        plt.plot(range(len(self.train_info)), [item[1] for item in self.train_info], 'r-')
        plt.ion()
        plt.show()
        plt.pause(0.05)
        #plt.show()
        if to_save:
            plt.savefig(save_fn)

    def log_train_info(self, save_fn='train_info.log'):
        logging.basicConfig(filename=save_fn, level=logging.INFO)
        for item in self.train_info:
            logging.info('batch {}, learning rate: {}, train loss: {}'.format(item[0], item[2], item[1]))

class InputDataFormat():
    FILE = 0,
    IMG_DATA = 1

class ExptConfigBase():
    
    model_params = DeepModelParamsBase()
    train_params = DeepModelTrainParamsBase()
    
    ''' task '''
    db_name = ''
    loss_name = 'clf'
    extra_info = ''
    # 0: file; 1: image data
    data_format = InputDataFormat.FILE
    # 0: train; 1: test
    mode = 0
    ''' extra params '''
    extra_params = {}

# base class for a task runner
# define each task to be executed
class ExptRunnerBase():
    ''' data '''
    train_data = None
    train_labels = None
    val_data = None
    val_labels = None
    test_data = None
    test_labels = None
    extra_data = {}
    expt_config = ExptConfigBase()
    ''' model '''
    model = BaseDeepModel(None, None)

    def __init__(self, expt_config):
        self.expt_config = expt_config

    # build model before preparing data
    def build_model(self):
        pass
    def prepare_data(self):
        pass
    def train_model(self):
        pass
    def test_model(self):
        pass
    def load_model(self):
        self.model.load_model(self.expt_config.train_params.model_fn)

# a template function to train and test a model
# mode 0: train; 1: test; 2: diagnose
# simply copy and paste it and customize as you like
def model_tester(mode):
    # load data
    #train_data, train_labels, test_data, test_labels = load_cifar10('E:/Projects/Github/deeplearning/Data/cifar-10-python/')

    model_fn = 'cifar_clf.pkl'
    # build model
    model = DummyModel(LossType.Classification)
    model.build_model()
    if mode == 0:
        # finetune
        # model.load_model(model_fn)
        model.learn_model(train_data, train_labels, test_data, test_labels, 100, 0.0001, 5)
        model.save_model(model_fn)
    if mode == 1:
        model.load_model(model_fn)
        model.eval_clf(test_data, test_labels)
    if mode == 2:
        model.load_model(model_fn)
        # add custom diagnose code


if __name__ == '__main__':
    pass
    
