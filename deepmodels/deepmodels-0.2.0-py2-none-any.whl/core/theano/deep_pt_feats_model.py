

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
from search_tools import *
from set_data_generator import *


# models to extract features?
class DeepPtFeaturesExptConfig(ExptConfigBase):
    model_params = ModelParamsBase()

    ''' test settings '''
    test_draw_distmat = False
    test_draw_codes = False
    test_draw_pr = True

    # given necessary info like db_name, loss_type etc
    # fill other params that depend on them
    def fill_params(self):
        self.feats_prefix = ''
        if self.model_params.flip_image:
            self.feats_prefix = self.feats_prefix+'flip'
        if self.model_params.crops_image:
            if not self.model_params.crops_image_nb:
                self.model_params.crops_image_nb = 5 # default value
            self.feats_prefix = self.feats_prefix+"crop"+str(self.model_params.crops_image_nb)
        self.extra_info = self.extra_info+self.feats_prefix
        self.train_params.model_fn_prefix = \
         'models/{}_pt_features_{}_{}'.format(self.db_name, self.loss_name, self.extra_info)
        self.train_params.model_fn = self.train_params.model_fn_prefix + '.pkl'


class BaseDeepFeatures(BaseModel):
    ''' data '''
    has_built_model = False

    ''' model I/O '''
    def save_model(self, save_fn):
        params = self.get_target_param_vals()
        data = {}
        data['param_vals'] = params
        data['class_names'] = self.class_names
        data['mean_img'] = self.mean_img
        with open(save_fn, 'wb') as f:
            pickle.dump(data, f)
        print('saved model to {}'.format(save_fn))

    def get_target_param_vals(self):
        return lasagne.layers.get_all_param_values(self.net[self.model_params.features_layer_name])

    def set_target_params(self, params):
        lasagne.layers.set_all_param_values(self.net[self.model_params.features_layer_name], params)

    # return boolean codes
    def encode_samples(self, samps, batch_sz=-1, input_type=InputDataFormat.IMG_DATA):
        outputs = lasagne.layers.get_output(self.net[self.model_params.features_layer_name])
        encode_fn = theano.function([self.net['input'].input_var], outputs)
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
                    #print 'encoding shape:
                    #{}'.format(samps[i:i+batch_sz].shape)
                    if input_type == InputDataFormat.FILE:
                        cur_samps = self.prepare_imgfns_for_input(samps[i:i + batch_sz])
                    else:
                        cur_samps = samps[i:i + batch_sz]
                    cur_codes = encode_fn(cur_samps)
                    if codes is None:
                        codes = cur_codes
                    else:
                        codes = np.vstack((codes, cur_codes))
        except Exception as e:
            print('encoding error: ' + str(e))
            raise Exception
        print 'encoding done.'
        return codes

class DeepPtFeaturesRunner(ExptRunnerBase):

    model = BaseDeepFeatures(None, None)
    expt_config = DeepPtFeaturesExptConfig()
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
                                   self.expt_config.train_params.batch_sz, self.expt_config.train_params.lrate,
                                   self.expt_config.train_params.num_epochs)
        # save model
        self.model.save_model(self.expt_config.train_params.model_fn)

    def test_model(self):
        self.load_model()
        # get test features
        if not os.path.exists('features'):
            os.mkdir('features')
        features_fn = 'features/test_features_{}_pt_features_{}_{}.pkl'.format(self.expt_config.db_name, self.expt_config.loss_name, self.expt_config.extra_info)
        if os.path.exists(features_fn) == False:
            # compute codes
            data = {}
            # form test point data
            if self.expt_config.data_format == InputDataFormat.FILE:
                if self.model.train_params.extra_input_info.has_key('test_bbox'):
                    self.model.train_params.extra_input_info['bbox'] = self.model.train_params.extra_input_info['test_bbox']
                self.test_imgs = self.model.prepare_imgfns_for_input(self.test_data)
            # encode
            test_pt_features = self.model.encode_samples(self.test_data, self.expt_config.train_params.batch_sz, False, InputDataFormat.FILE)
            data['test_pt_labels'] = self.test_labels
            data['test_pt_features'] = test_pt_features
            pickle.dump(data, open(features_fn, 'wb'))

        # load codes
        print('Loading precomputed features')
        data = pickle.load(open(features_fn,'rb'))
        test_features = data['test_pt_features']
        test_all_labels = data['test_pt_labels']
        test_all_labels = np.asarray(test_all_labels)

        cls_labels = gen_cls_labels(test_all_labels)
        # draw codes
        if self.expt_config.test_draw_codes:
            for label, ids in cls_labels.iteritems():
                plt.figure()
                plt.imshow(test_features[ids], cmap='jet', aspect='auto')
                if not os.path.exists('visfeatures'):
                    os.mkdir('visfeatures')
                save_fn = 'visfeatures/{}_pt_features_{}_label_{}_test_{}.png'.format(self.expt_config.db_name, self.expt_config.loss_name, label, self.expt_config.extra_info)
                plt.savefig(save_fn)
            print 'features drawn'

        order_ids = []
        for label, ids in cls_labels.iteritems():
            if len(order_ids) == 0:
                order_ids = ids
            else:
                order_ids = np.hstack((order_ids,ids))
        dist_mat = comp_distmat(test_features[order_ids], None, DistType.L2)
        # visualize distance matrix
        if self.expt_config.test_draw_distmat:
            if not os.path.exists('dists'):
                    os.mkdir('dists')
            save_fn = 'dists/{}_pt_features_{}_{}_test.png'.format(self.expt_config.db_name, self.expt_config.loss_name, self.expt_config.extra_info)
            plt.figure()
            plt.imshow(dist_mat, cmap='jet', aspect='auto')
            plt.colorbar()
            plt.savefig(save_fn)
        # pr curve
        if self.expt_config.test_draw_pr:
            if not os.path.exists('res'):
                    os.mkdir('res')
            evaluate('res/{}_pt_features_{}_{}_test'.format(\
                self.expt_config.db_name, self.expt_config.loss_name, self.expt_config.extra_info),
                     dist_mat, test_all_labels[order_ids], test_all_labels[order_ids],
                     'res/{}_pt_features_{}_{}_test.png'.format(\
                         self.expt_config.db_name, self.expt_config.loss_name, self.expt_config.extra_info))
