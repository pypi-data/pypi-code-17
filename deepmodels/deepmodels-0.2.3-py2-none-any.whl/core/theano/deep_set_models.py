

import sys
import os
import gzip
import cPickle as pickle
from sets import Set
import random
import numpy as np
import time
import matplotlib.pyplot as plt

import theano
import theano.typed_list
import theano.tensor as T
#import theano.compile.nanguardmode
import lasagne
from lasagne.layers import InputLayer, DenseLayer, DropoutLayer
from lasagne.layers import NonlinearityLayer
from lasagne.layers import Conv2DLayer as ConvLayer
#from lasagne.layers.dnn import Conv2DDNNLayer as ConvLayer
from lasagne.layers import LocalResponseNormalization2DLayer as NormLayer
from lasagne.nonlinearities import softmax, sigmoid, rectify

from model_tools import *
from model_factory import ModelType, ModelFactory
from data_manager import *
from base_model import *
from deep_matcher import TripletDist
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath) + '/../'
sys.path.append(dname)
from search_tools import *
from set_data_generator import *
from deep_pt_hash_models import *
from deep_clf import DeepClf
from deep_matcher import DeepMatcher
from hasher import *

''' set based model '''

class SetAggregationType:
    MEAN = 0,
    COV_MAT = 1,
    VAR = 2,
    MIN = 3,
    MAX = 4,
    VLAD = 5,
    PCA = 6

class AggregationLayerMean(lasagne.layers.Layer):
    def get_output_for(self, input, **kwargs):
        mean_val = T.mean(input, axis=0, keepdims=True)
        return mean_val
    def get_output_shape_for(self, input_shape):
        return [1, input_shape[1]]

class AggregationLayerCovMat(lasagne.layers.Layer):
    def get_output_for(self, input, **kwargs):
        var = T.var(input, axis=None)
        return T.reshape(var, (1,))
    def get_output_shape_for(self, input_shape):
        return input_shape[1]

# set specific layer
# input layer needs to be flattened
class AggregationLayerAll(lasagne.layers.Layer):
    def get_output_for(self, input, **kwargs):
        mean_val = T.mean(input, axis=0, keepdims=True)
        #var = T.var(input, axis=0)  # only variance in one dim
        min_val = T.min(input, axis=0, keepdims=True)
        max_val = T.max(input, axis=0, keepdims=True)
        res = T.concatenate([mean_val, min_val, max_val], axis=0)
        return res
    def get_output_shape_for(self, input_shape):
        return [1, input_shape[1]*3]


class AggregationLayerBoW(lasagne.layers.Layer):
    def get_output_for(self, input, kmeans_dict, **kwargs):
        ''' compute vlad x
            for each feature, compute x-c(x)
            sum and average
        '''
        input_cls = kmeans_dict.predict(input)
        input_diff = np.zeros((input.shape[0], input.shape[1]), np.float32)
        for i in range(len(input)):
            input_diff[i,:] = input[i] - kmeans_dict.cluster_centers_[input_cls[i]]
        
        vlad_feat = np.mean(input_diff, axis=0)
        return vlad_feat

    def get_output_shape_for(self, input_shape):
        # fixed dict size
        return [1, 128]

# most general set-based model params
class DeepSetParams(ModelParamsBase):
    pass

# basic set based model with
class DeepSet(BaseModel):
    def prepare_setfns_for_input(self, set_fns, extra_info=None):
        set_data = []
        for img_set in set_fns:
            cur_set_imgs = self.prepare_imgfns_for_input(img_set, extra_info)
            set_data.append(cur_set_imgs)
        return np.asarray(set_data)
        
    def learn_set_model_large_scale(self, train_set_fns, train_labels, val_set_fns, val_labels):
        # val_img_fns, val_labels are not used?
        train_img_fns = np.asarray(train_set_fns)
        train_labels = np.asarray(train_labels)
        print 'training in large scale mode'
        self.create_iter_funcs(self.train_params.lrate)
        train_loss = 0
        train_batches = 0
        for epoch in range(self.train_params.num_epochs):
            batch_num = 0
            # randomize
            ids = range(len(train_labels))
            np.random.shuffle(ids)
            img_fns = train_img_fns[ids]
            labels = train_labels[ids]
            # run each batch
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
                sets = self.prepare_setfns_for_input(cur_batch_fns, self.train_params.extra_input_info)
                if sets.shape[0] != cur_batch_labels.size:
                    print 'set and label number not consistent, skip this batch'
                    continue
                print("batch data prepare time: {:.3f}s".format(time.time() - batch_data_prepare_start))
                train_loss += self.learn_model(sets, cur_batch_labels, None, None, 1)
                print("total batch time: {:.3f}s".format(time.time() - train_batch_startt))
                print 'epoch {}, batch {} loss: \t\t{:.8f}'.format(epoch+1, train_batches, train_loss / train_batches)
                if train_loss / train_batches <= self.train_params.stop_loss:
                    break
            
            if np.mod(epoch, self.train_params.step_save)==0:
                tmp_fn = self.train_params.model_fn_prefix + '_iter' + str(train_batches) + '.pkl'
                self.save_model(tmp_fn)
            if train_loss / train_batches <= self.train_params.stop_loss:
                break
        
# [obsolete]     
class BaseDeepSetModel(BaseModel):
    model_params = DeepSetParams()

    # build from stratch or based on base model
    def build_set_model(self):
        pass

    # train_imgset_fns: a list of array of filenames
    # def learn_model_large_scale(self, train_imgset_fns, train_set_labels, val_imgset_fns, val_set_labels):
    #    print 'training in large scale mode'
    #    self.create_iter_funcs(self.train_params.lrate)
    #    train_loss = 0
    #    train_batches = 0
    #    for epoch in range(self.train_params.num_epochs):
    #        batch_num = 0
    #        # randomize
    #        ids = range(len(train_set_labels))
    #        np.random.shuffle(ids)
    #        imgset_fns = [train_imgset_fns[id] for id in ids]
    #        labels = [train_set_labels[id] for id in ids]
    #        for id in range(0, len(imgset_fns)-self.train_params.batch_sz, self.train_params.batch_sz):
    #            train_batches += 1
    #            batch_num += 1
    #            print('processing epoch {} batch {}'.format(epoch, batch_num))
    #            train_batch_startt = time.time()
    #            # decrease learning rate after certain iters
    #            if batch_num % self.train_params.step_lr == 0 and self.train_params.lrate >= 0.0001:
    #                tmp_fn = self.train_params.model_fn_prefix + '_iter' + str(batch_num) + '.pkl'
    #                self.save_model(tmp_fn)
    #                self.train_params.lrate *= self.train_params.gamma_lr
    #                self.create_iter_funcs(self.train_params.lrate)
                
    #            batch_data_prepare_start = time.time()
    #            cur_batch_set_fns = imgset_fns[id:id+self.train_params.batch_sz]
    #            cur_batch_set_labels = labels[id:id+self.train_params.batch_sz]
    #            img_sets = self.prepare_imgfns_for_input(cur_batch_set_fns, self.train_params.extra_input_info)
    #            assert len(img_sets) == len(cur_batch_set_labels)
    #            print("batch data prepare time: {:.3f}s".format(time.time() - batch_data_prepare_start))
    #            train_loss += self.learn_model(img_sets, cur_batch_set_labels, None, None, 1)
    #            print("total batch time: {:.3f}s".format(time.time() - train_batch_startt))
    #            print 'epoch {}, batch {} loss: \t\t{:.8f}'.format(epoch, train_batches, train_loss / train_batches)


class DeepSetClf(DeepClf, DeepSet):
    def create_iter_train_func(self, lrate):
        target_var = T.ivector('train_targets')
        tl = theano.typed_list.TypedListType(self.net['input'].input_var.type)()
        # go through model to get output for each set input
        len = theano.typed_list.length(tl)
        train_loss = T.fscalar('train_loss')
        cnt = 0
        for i in range(self.train_params.batch_sz):
            output = lasagne.layers.get_output(self.net[self.model_params.output_layer_name], inputs=tl[i])
            if cnt == 0:
                outputs = output
            else:
                outputs = T.concatenate([outputs, output], axis=0)
            cnt += 1
        loss = lasagne.objectives.categorical_crossentropy(outputs, target_var)
        train_loss = loss.mean()
        params = self.get_target_params(for_training=True)
        print('total trainable parameter number: {}'.format(lasagne.layers.count_params(self.net[self.model_params.output_layer_name])))
        print('train with learning rate: {:.6f}'.format(lrate))
        updates = lasagne.updates.nesterov_momentum(train_loss, params, learning_rate=lrate, momentum=0.9)
        start = time.time()
        train_fn = theano.function([tl, target_var], train_loss, updates=updates)
        elapsed = time.time() - start
        print 'training function compiled: ',str(elapsed)
        
        return train_fn
        

    
class DeepSetMatcher(DeepMatcher):
    def create_iter_train_func(self, lrate):
        tl = theano.typed_list.TypedListType(self.net['input'].input_var.type)()
        # go through model to get output for each set input
        len = theano.typed_list.length(tl)
        train_loss = T.fscalar('train_loss')
        cnt = 0
        for i in range(self.train_params.batch_sz):
            output = lasagne.layers.get_output(self.net[self.model_params.output_layer_name], inputs=tl[i])
            if cnt == 0:
                outputs = output
            else:
                outputs = T.concatenate([outputs, output], axis=0)
            cnt += 1
        # compute triplet loss
        if hasattr(self.train_params, 'triplet_dist') and self.train_params.triplet_dist==TripletDist.L1:
            # L1
            dist1 = (abs(outputs[::3]-outputs[1::3])).sum(axis=1)
            dist2 = (abs(outputs[::3]-outputs[2::3])).sum(axis=1)
        else:
            # L2
            dist1 = ((outputs[::3]-outputs[1::3])**2).sum(axis=1)
            dist2 = ((outputs[::3]-outputs[2::3])**2).sum(axis=1)
        dist = dist1 - dist2 + self.train_params.triplet_margin
        samp_sgn = T.gt(dist, 0.0)
        train_loss = T.sum(dist * samp_sgn) / T.shape(outputs)[0]*3
        # compute percentage of triplet with loss 0
        useful_num = samp_sgn.sum()
        # updates for training
        #params = lasagne.layers.get_all_params(self.net['output'], trainable=True)
        params = self.get_target_params(for_training=True)
        #print('total trainable parameter number: {}'.format(lasagne.layers.count_params(self.net['output'])))
        print('total trainable parameter number: {}'.format(lasagne.layers.count_params(self.net[self.model_params.output_layer_name])))
        print('train with learning rate: {:.6f}'.format(lrate))
        updates = lasagne.updates.nesterov_momentum(train_loss, params, learning_rate=lrate, momentum=0.9)
        # functions
        start_comp = time.time()
        train_fn = theano.function(
            [tl], 
            train_loss, updates=updates)
        print "Train function compilation took:",str(time.time()-start_comp)+"s."
        return train_fn

# params for set based hash model
class DeepSetHashParams(DeepSetParams, DeepHasherParams):
    pass


class DeepSetHashExptConfig(ExptConfigBase):

    model_params = DeepSetHashParams()

    ''' test settings '''
    test_draw_distmat = False
    test_draw_codes = False
    test_draw_pr = False

    def fill_params(self):
        self.train_params.model_fn_prefix = \
         './models/{}_set_hash_{}bit_{}_{}'.format(self.db_name, self.model_params.code_dims, self.loss_name, self.extra_info)
        self.train_params.model_fn = self.train_params.model_fn_prefix + '.pkl'

# multi-layer set based deep hash model
class DeepSetClfMLHasher(DeepSetClf, MLHasher):
    model_params = DeepSetHashParams()
    
    ''' steps to build a set hash model
        1. build base model using build_model
        2. build set model
        3. build hash model
    '''
    def build_set_model(self):
        pass
    def build_hash_model(self):
        #self.build_set_model()
        for i in range(len(self.model_params.code_dims)):
            dst_layer_name = ''
            src_layer_name = ''
            if i == 0:
                # first and last
                if len(self.model_params.code_dims)==1:
                    dst_layer_name = self.model_params.hash_layer_name
                    src_layer_name = self.model_params.prev_hash_layer
                    self.net[dst_layer_name] = DenseLayer(self.net[src_layer_name], num_units=self.model_params.code_dims[i], nonlinearity=sigmoid)
                else:
                    dst_layer_name = 'hash_' + str(i)
                    src_layer_name = self.model_params.prev_hash_layer
                    self.net[dst_layer_name] = DenseLayer(self.net[src_layer_name], num_units=self.model_params.code_dims[i], nonlinearity=rectify)
            elif i == len(self.model_params.code_dims)-1:
                # last layer
                dst_layer_name = self.model_params.hash_layer_name
                src_layer_name = 'hash_' + str(i-1)
                self.net[dst_layer_name] = DenseLayer(self.net[src_layer_name], num_units=self.model_params.code_dims[i], nonlinearity=sigmoid)
            else:
                # middle layer
                dst_layer_name = 'hash_' + str(i)
                src_layer_name = 'hash_' + str(i-1)
                self.net[dst_layer_name] = DenseLayer(self.net[src_layer_name], num_units=self.model_params.code_dims[i], nonlinearity=rectify)          
        print self.net.keys()
        
        if self.train_params.loss_type == LossType.Triplet:
            # for triplet loss
            self.net['output'] = NonlinearityLayer(self.net[self.model_params.hash_layer_name], nonlinearity=identity)
        if self.train_params.loss_type == LossType.Classification:
            # for classification loss
            print 'classification class: {}'.format(self.model_params.cls_num)
            self.net['output'] = DenseLayer(self.net[self.model_params.hash_layer_name], num_units=self.model_params.cls_num, nonlinearity=softmax)

    def encode_sets(self, set_samps, binary=True):
        outputs = lasagne.layers.get_output(self.net[self.model_params.hash_layer_name])
        if binary:
            code = outputs > 0.5
        else:
            code = outputs
        encode_fn = theano.function([self.net['input'].input_var], code)
        codes = []
        print 'start encoding'
        cnt = 0
        for cur_set in set_samps:
            code = encode_fn(cur_set)
            #code = code.astype(np.bool_)
            codes.append(code)
            cnt += 1
            if cnt % 100 == 0:
                print '{}/{}'.format(cnt, set_samps.shape[0])
        print 'encoding done.'
        return np.concatenate(codes, axis=0)


class DeepSetHashRunner(ExptRunnerBase):
    model = DeepSetClfMLHasher(None, None)
    expt_config = DeepSetHashExptConfig()

    # train_data and test_data have to be set data
    test_gal_data = None
    test_gal_labels = None
    test_probe_data = None
    test_probe_labels = None

    def train_model(self):
        if self.expt_config.data_format == InputDataFormat.FILE:
            if self.model.train_params.extra_input_info.has_key('train_bbox'):
                self.model.train_params.extra_input_info['bbox'] = self.model.train_params.extra_input_info['train_bbox']
            self.model.learn_model_large_scale(self.train_data, self.train_labels, 
                                               self.val_data, self.val_labels)
        if self.expt_config.data_format == InputDataFormat.IMG_DATA:
            self.model.learn_model(self.train_data, self.train_labels, self.val_data, self.val_labels, self.expt_config.train_params.num_epochs)
        
        self.model.draw_train_info(True, self.model.train_params.model_fn_prefix + '_traininfo.png')
        # save model
        self.model.save_model(self.expt_config.train_params.model_fn)

    def test_model(self):
        self.load_model()
        # get test codes
        code_fn = 'codes/test_codes_{}_set_hash_{}_{}_{}.pkl'.format(\
            self.expt_config.db_name, self.expt_config.model_params.code_dims, self.expt_config.loss_name, self.expt_config.extra_info)
        #if os.path.exists(code_fn) == False:
        # compute codes
        data = {}
        # encode
        if self.expt_config.data_format == InputDataFormat.FILE:
            if self.model.train_params.extra_input_info.has_key('test_bbox'):
                self.model.train_params.extra_input_info['bbox'] = self.model.train_params.extra_input_info['test_bbox']
            self.test_imgs = self.model.prepare_imgfns_for_input(self.test_data)
        else:
            self.test_imgs = np.asarray(self.test_data)
        #ids = range(1000)
        test_set_codes = self.model.encode_sets(self.test_imgs)
        data['test_set_labels'] = np.asarray(self.test_labels)
        data['test_set_codes'] = test_set_codes
        pickle.dump(data, open(code_fn, 'wb'))

        # load codes
        print 'Loading precomputed codes'
        data = pickle.load(open(code_fn,'rb'))
        test_set_codes = data['test_set_codes']
        test_all_labels = data['test_set_labels']
        print 'precomputed codes loaded'
        
        cls_labels = gen_cls_labels(test_all_labels)
        # draw codes
        if self.expt_config.test_draw_codes == True:
            for label, ids in cls_labels.iteritems():
                plt.figure()
                plt.imshow(test_set_codes[ids], cmap='jet', aspect='auto')
                save_fn = 'viscodes/{}_set_codes_{}_label_{}_test_{}.png'.format(\
                    self.expt_config.db_name, self.expt_config.loss_name, label, self.expt_config.extra_info)
                plt.savefig(save_fn)
            print 'codes drawn'
        order_ids=[]
        for label, ids in cls_labels.iteritems():
            if len(order_ids)==0:
                order_ids=ids
            else:
                order_ids=np.hstack((order_ids,ids))

        dist_mat = comp_distmat(test_set_codes[order_ids], None)
        # visualize distance matrix
        if self.expt_config.test_draw_distmat:
            save_fn = 'dists/{}_set_hash_{}_{}_{}_test.png'.format(\
                self.expt_config.db_name, self.expt_config.model_params.code_dims[-1], \
                self.expt_config.loss_name, self.expt_config.extra_info)
            plt.figure()
            plt.imshow(dist_mat, cmap='jet', aspect='auto')
            plt.colorbar()
            plt.savefig(save_fn)
        # pr curve
        if self.expt_config.test_draw_pr:
            evaluate('{}_set_hash_{}_{}_{}_test'.format(\
                self.expt_config.db_name, self.expt_config.model_params.code_dims, self.expt_config.loss_name, self.expt_config.extra_info), 
                     dist_mat, test_all_labels[order_ids], test_all_labels[order_ids], 
                     'res/{}_set_hash_{}_{}_{}_test.png'.format(\
                         self.expt_config.db_name, self.expt_config.model_params.code_dims, self.expt_config.loss_name, self.expt_config.extra_info))
