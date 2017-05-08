
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
from lasagne.nonlinearities import softmax, sigmoid, rectify, identity, leaky_rectify

from model_tools import *
from model_factory import ModelType, ModelFactory
from data_manager import *
from base_model import *
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath) + '/../'
sys.path.append(dname)
from search_tools import *
from set_data_generator import *

from hasher import DeepHasherParams


# only net['hash'] is responsible to produce hash codes; it outputs 0~1 real value
class BaseDeepHasher(BaseModel):
    ''' data '''
    has_built_model = False
    model_params = DeepHasherParams()

    def build_hash_model(self):
        pass
    
    # return boolean codes
    def encode_samples(self, samps, batch_sz=-1, binary=True, input_type=InputDataFormat.IMG_DATA):
        outputs = lasagne.layers.get_output(self.net[self.model_params.hash_layer_name])
        if binary:
            code = outputs > 0.5
        else:
            code = outputs
        encode_fn = theano.function([self.net['input'].input_var], code)
        try:
            codes = None
            if batch_sz == -1:
                codes = encode_fn(samps)
            else:
                samp_num = 0
                if input_type == InputDataFormat.FILE:
                    samp_num = len(samps)
                if input_type == InputDataFormat.IMG_DATA:
                    samp_num = samps.shape[0]
                for i in np.arange(0, samp_num, batch_sz):
                    #print 'encoding shape: {}'.format(samps[i:i+batch_sz].shape)
                    if input_type == InputDataFormat.FILE:
                        cur_samps = self.prepare_imgfns_for_input(samps[i:i+batch_sz])
                    else:
                        cur_samps = samps[i:i+batch_sz]
                    cur_codes = encode_fn(cur_samps)
                    if codes is None:
                        codes = cur_codes
                    else:
                        codes = np.vstack((codes, cur_codes))
            # conver to boolean
            if binary:
                codes = codes.astype(np.bool_)
        except Exception as e:
            print('encoding error: '+str(e))
            raise Exception
        print 'encoding done.'
        return codes

# multi-layer hash model, generic for point or set
class DeepMLHasher(BaseDeepHasher):
    # build hash layers
    def build_hash_model(self):
        #self.build_model()
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
                    # how to set different rectify unit?
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
            self.net['output'] = DenseLayer(self.net[self.model_params.hash_layer_name], num_units=self.model_params.cls_num, nonlinearity=softmax)


class DeepPtHashExptConfig(ExptConfigBase):
    model_params = DeepHasherParams()
  
    ''' test settings '''
    test_draw_distmat = False
    test_draw_codes = False
    test_draw_pr = True

    # given necessary info like db_name, loss_type etc
    # fill other params that depend on them
    def fill_params(self):
        if self.train_params.loss_type == LossType.Classification:
            self.loss_name = 'clf'
        elif self.train_params.loss_type == LossType.Triplet:
            self.loss_name = 'triplet'
        elif self.train_params.loss_type == LossType.TripletClassification:
            self.loss_name = 'triplet_clf'
        else:
            print "Beware, unknown loss_type:",str(self.train_params.loss_type)
        self.train_params.model_fn_prefix = \
         'models/{}_pt_hash_{}_{}_{}'.format(self.db_name, '-'.join([str(x) for x in self.model_params.code_dims]), self.loss_name, self.extra_info)
        self.train_params.model_fn = self.train_params.model_fn_prefix + '.pkl'


class DeepPtHashRunner(ExptRunnerBase):

    model = BaseDeepHasher(None, None)
    expt_config = DeepPtHashExptConfig()
    # search related data structure
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
            self.model.learn_model(self.train_data, self.train_labels, self.val_data, self.val_labels,
                                   self.expt_config.train_params.num_epochs)
        # save model
        self.model.save_model(self.expt_config.train_params.model_fn)

    def test_model(self):
        self.load_model()
        # get test codes
        code_fn = 'codes/test_codes_{}_pt_hash_{}_{}_{}.pkl'.format(
            self.expt_config.db_name, self.expt_config.model_params.code_dims, self.expt_config.loss_name, self.expt_config.extra_info)
        if os.path.exists(code_fn) == False:
            # compute codes
            data = {}
            # form test point data
            if self.expt_config.data_format == InputDataFormat.FILE:
                if self.model.train_params.extra_input_info.has_key('test_bbox'):
                    self.model.train_params.extra_input_info['bbox'] = self.model.train_params.extra_input_info['test_bbox']
                self.test_imgs = self.model.prepare_imgfns_for_input(self.test_data)
            # encode
            test_gal_codes = self.model.encode_samples(self.test_gal_data, self.expt_config.train_params.batch_sz, True, InputDataFormat.IMG_DATA)
            data['test_gal_labels'] = self.test_gal_labels
            data['test_gal_codes'] = test_gal_codes
            test_probe_codes = self.model.encode_samples(self.test_probe_data, self.expt_config.train_params.batch_sz, True, InputDataFormat.IMG_DATA)
            data['test_probe_labels'] = self.test_probe_labels
            data['test_probe_codes'] = test_probe_codes
            pickle.dump(data, open(code_fn, 'wb'))

        # load codes
        print('Loading precomputed codes')
        data = pickle.load(open(code_fn,'rb'))
        test_gal_codes = data['test_gal_codes']
        test_gal_labels = data['test_gal_labels']
        test_probe_codes = data['test_probe_codes']
        test_probe_labels = data['test_probe_labels']
        
        cls_labels = gen_cls_labels(test_gal_labels)
        # draw codes
        if self.expt_config.test_draw_codes:
            for label, ids in cls_labels.iteritems():
                plt.figure()
                plt.imshow(test_gal_codes[ids], cmap='jet', aspect='auto')
                save_fn = 'viscodes/{}_pt_codes_{}_label_{}_test_{}.png'.format(
                    self.expt_config.db_name, self.expt_config.loss_name, label, self.expt_config.extra_info)
                plt.savefig(save_fn)
            print 'codes drawn'
        
        #order_ids=[]
        #for label, ids in cls_labels.iteritems():
        #    if len(order_ids)==0:
        #        order_ids=ids
        #    else:
        #        order_ids=np.hstack((order_ids,ids))
        dist_mat = comp_distmat(test_probe_codes, test_gal_codes, DistType.Hamming)
        # visualize distance matrix
        if self.expt_config.test_draw_distmat:
            save_fn = 'dists/{}_pt_hash_{}_{}_{}_test.png'.format(
                self.expt_config.db_name, self.expt_config.model_params.code_dims, 
                self.expt_config.loss_name, self.expt_config.extra_info)
            plt.figure()
            plt.imshow(dist_mat, cmap='jet', aspect='auto')
            plt.colorbar()
            plt.savefig(save_fn)
        # pr curve
        if self.expt_config.test_draw_pr:
            evaluate('res/{}_pt_hash_{}_{}_{}_test'.format(\
                self.expt_config.db_name, self.expt_config.model_params.code_dims, self.expt_config.loss_name, self.expt_config.extra_info), 
                     dist_mat, test_gal_labels, test_probe_labels, 
                     'res/{}_pt_hash_{}_{}_{}_test.png'.format(\
                         self.expt_config.db_name, self.expt_config.model_params.code_dims, self.expt_config.loss_name, self.expt_config.extra_info))

    def test_model_on_sets(self):
        self.load_model()
        code_fn = 'codes/test_codes_{}_pt_hash_{}_{}_{}.pkl'.format(
            self.expt_config.db_name, self.expt_config.model_params.code_dims, self.expt_config.loss_name, self.expt_config.extra_info)
        if os.path.exists(code_fn) == False:
            # compute codes
            data = {}
            # form test point data
            if self.expt_config.data_format == InputDataFormat.FILE:
                self.model.train_params.extra_input_info['bbox'] = self.model.train_params.extra_input_info['test_bbox']
                self.test_imgs = self.model.prepare_imgfns_for_input(self.test_data)
            # encode
            test_set, test_set_labels = gen_real_sets(self.test_data, self.test_labels, None, 5)
            #test_set, test_set_labels = gen_mixed_sets(self.test_data, self.test_labels, None, 5, 5, [AugmentType.Crop])
            #test_set, test_set_labels = form_sets(self.test_data, self.test_labels, 5)
            test_set_codes = []
            for i in range(len(test_set)):
                print 'encoding test set: {}'.format(i)
                test_set_codes.append(self.model.encode_samples(test_set[i]))
            data['test_set_labels'] = test_set_labels
            data['test_set_codes'] = test_set_codes
            pickle.dump(data, open(code_fn, 'wb'))
        
        # load codes
        print 'Loading precomputed codes'
        data = pickle.load(open(code_fn,'rb'))
        test_set_codes = data['test_set_codes']
        test_set_labels = data['test_set_labels']
        test_set_labels = np.asarray(test_set_labels)
        print 'precomputed codes loaded'

        # matching sets using points
        cls_labels = gen_cls_labels(test_set_labels)
        order_ids = []
        for label, ids in cls_labels.iteritems():
            if len(order_ids) == 0:
                order_ids = ids
            else:
                order_ids = np.hstack((order_ids, ids))    
        test_set_codes = [test_set_codes[id] for id in order_ids]
        dist_mat = match_set_with_pts(test_set_codes, test_set_codes, PtSetDist.Min)

        if self.expt_config.test_draw_pr:
                evaluate('{}_pt_hash_{}_{}_{}_test'.format(\
                self.expt_config.db_name, self.expt_config.model_params.code_dims, self.expt_config.loss_name, self.expt_config.extra_info), 
                     dist_mat, test_set_labels[order_ids], test_set_labels[order_ids], 
                     'res/{}_pt_hash_{}_{}_{}_test.png'.format(\
                         self.expt_config.db_name, self.expt_config.model_params.code_dims, self.expt_config.loss_name, self.expt_config.extra_info))
