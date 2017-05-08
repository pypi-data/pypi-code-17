
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
import theano.tensor as T
import theano.compile.nanguardmode
import lasagne
from lasagne.layers import InputLayer, DenseLayer, DropoutLayer
from lasagne.layers import NonlinearityLayer
from lasagne.layers import Conv2DLayer as ConvLayer
#from lasagne.layers.dnn import Conv2DDNNLayer as ConvLayer
from lasagne.layers import MaxPool2DLayer as PoolLayer
from lasagne.layers import LocalResponseNormalization2DLayer as NormLayer
from lasagne.nonlinearities import softmax, identity, sigmoid

from ModelTools import prepare_img_for_test
from ModelFactory import ModelType, ModelFactory
from DataManager import gen_cls_combs, gen_random_triplets, gen_samps_from_cls, gen_hard_triplets
from BaseDeepModel import BaseDeepModel, LossType
from base_custom_models import BaseMultiLossDeepModel, BaseMultiLossDeepHasher


class L2NormLayer(lasagne.layers.Layer):
    def get_output_for(self, input, **kwargs):
        res = T.printing.Print('Normalized hash codes:')(input/(np.sqrt((input**2).sum(axis=0))))
        return res
    def get_output_shape_for(self, input_shape):
        return input_shape


class TripletClfLossHasher(BaseMultiLossDeepHasher):

    def build_model(self):
        pass

    def build_hash_model(self):
        pass

    def build_hash_class_model(self):
        self.net['hash'] = DenseLayer(self.net['dropout4'], num_units=self.code_len, nonlinearity=sigmoid)
        if self.loss_type == LossType.Triplet:
            # for triplet loss
            self.net['output'] = NonlinearityLayer(self.net['hash'], nonlinearity=identity)
        if self.loss_type == LossType.Classification:
        # for classification loss
            self.net['output'] = DenseLayer(self.net['hash'], num_units=self.cls_num, nonlinearity=softmax)
        if self.loss_type == LossType.TripletClassification:
        # for triplet-classification loss
            self.net['output'] = NonlinearityLayer(self.net['hash'], nonlinearity=identity)
            self.net['class'] = DenseLayer(self.net['hash'], num_units=self.cls_num, nonlinearity=softmax)


    def create_iter_train_func(self, lrate):
        print('train with learning rate: {:.6f}'.format(lrate))
        # compute classification loss
        target_var = T.ivector('train_targets')
        train_output = lasagne.layers.get_output(self.net['class'])
        train_loss_tmp = lasagne.objectives.categorical_crossentropy(train_output, target_var)
        train_loss_class = train_loss_tmp.mean()
        # triplet loss
        # output are stacked: repeating (anchor, similar, dissimilar)
        output = lasagne.layers.get_output(self.net['output'])
        dist1 = ((output[::3]-output[1::3])**2).sum(axis=1)
        dist2 = ((output[::3]-output[2::3])**2).sum(axis=1)
        dist = dist1 - dist2 + self.triplet_margin
        samp_sgn = T.gt(dist, 0.0)
        triplet_loss = T.printing.Print('triplet_loss is:')(T.sum(dist * samp_sgn)/T.shape(output)[0]*3)
        # updates for training
        params = lasagne.layers.get_all_params(self.net['class'], trainable=True)
        print('total trainable parameter number: {}'.format(lasagne.layers.count_params(self.net['class'])))
        updates = lasagne.updates.nesterov_momentum(train_loss_class+triplet_loss, params, learning_rate=lrate, momentum=0.9)
        # functions
        train_fn = theano.function([self.net['input'].input_var, target_var],
                                    train_loss_class+triplet_loss, updates=updates,name="train_triplet")
        return train_fn

