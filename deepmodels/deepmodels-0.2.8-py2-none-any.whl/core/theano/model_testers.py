# testing various basic models
# jiefeng@2015-10-15

import sys
import os
import gzip
import math
#sys.path.append('E:/Projects/Github/deeplearning/Theano/Lasagne/tools/')
from data_manager import form_metadata_from_folder, split_train_val_test, \
    load_mnist, load_cifar10, load_imgs, batch_prepare_imgs, form_set_data, gen_cls_combs, \
    gen_samps_from_cls, gen_hard_triplets, gen_random_triplets
import theano
import theano.typed_list
import theano.tensor as T
import theano.compile.nanguardmode
import lasagne
import cPickle as pickle
from sets import Set
import random
import numpy as np
import time
import cv2
import scipy
import sklearn
import matplotlib.pyplot as plt

from lasagne.layers import InputLayer, DenseLayer, DropoutLayer
from lasagne.layers import NonlinearityLayer
from lasagne.layers import Conv2DLayer as ConvLayer
#from lasagne.layers.dnn import Conv2DDNNLayer as ConvLayer
from lasagne.layers import MaxPool2DLayer as PoolLayer
from lasagne.layers import Pool2DLayer
from lasagne.layers import LocalResponseNormalization2DLayer as NormLayer
from lasagne.nonlinearities import softmax, sigmoid

from model_factory import ModelType, ModelFactory
from BaseDeepModel import BaseDeepModel
from ModelTools import prepare_img_for_test


''' NEED TO BE INTEGRATED TO NEW CLASS STRUCTURES '''

class CIFARModel(BaseDeepModel):
    
    def build_model(self):
        factory = ModelFactory()
        self.net = factory.build_cifar10()

def train_cifar10():
    # load data
    train_data, train_labels, test_data, test_labels = load_cifar10('E:/Projects/Github/deeplearning/Data/cifar-10-python/')

    mode = 0
    model_fn = 'cifar_clf.pkl'
    # build model
    model = CIFARModel()
    model.build_model()
    model.load_model(model_fn)
    if mode == 0:
        model.learn_model(train_data, train_labels, test_data, test_labels, 100, 0.0001, 5)
        model.save_model(model_fn)
    else:
        model.load_model(model_fn)
        model.eval_clf(test_data, test_labels)

if __name__ == '__main__':
    train_cifar10()