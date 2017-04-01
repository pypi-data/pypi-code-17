'''
construct hashing model
'''

from common import InputDataFormat, LossType, NormType
from base_model import ModelParamsBase

import time
import numpy as np
import theano
import lasagne
from lasagne.layers import InputLayer, DenseLayer, DropoutLayer, NonlinearityLayer
from lasagne.nonlinearities import sigmoid, softmax, rectify, identity

# to add hashing function, simple inherit from one hasher

# point based hashing
class DeepHasherParams(ModelParamsBase):
    # dimensions of multilayers
    code_dims = [32]
    output_layer_name = 'hash'
    prev_hash_layer = ''  # layer name before hashing
    hash_layer_name = 'hash'

class BaseHasher():
    encode_fn = None
    
    def build_hash_model(self):
        pass
        
    # samps are a tensor
    def encode_samples(self, samps, batch_sz=-1, input_type=InputDataFormat.IMG_DATA, norm_type=None):     
        # build encoding function
        if self.encode_fn == None:     
            outputs = lasagne.layers.get_output(self.net[self.model_params.hash_layer_name])
            if norm_type == NormType.L2:
                outputs = outputs / outputs.norm(2, axis=1).reshape((outputs.shape[0],1))
            if norm_type == NormType.L1:
                outputs = outputs / outputs.norm(1, axis=1).reshape((outputs.shape[0],1))
            # binarize
            codes = outputs > 0.5
            self.encode_fn = theano.function([self.net['input'].input_var], codes)
        
        # encode
        try:
            all_codes = None
            samp_num = 0
            if input_type == InputDataFormat.FILE:
                samp_num = len(samps)
            if input_type == InputDataFormat.IMG_DATA:
                samp_num = samps.shape[0]
            
            if batch_sz == -1:
                batch_sz = samp_num
            startt = time.time()
            for i in np.arange(0, samp_num, batch_sz):
                #print 'encoding shape: {}'.format(samps[i:i+batch_sz].shape)
                if input_type == InputDataFormat.FILE:
                    cur_samps = self.prepare_imgfns_for_input(samps[i:i+batch_sz])
                else:
                    cur_samps = samps[i:i+batch_sz]
                cur_codes = self.encode_fn(cur_samps)
                if all_codes is None:
                    all_codes = cur_codes
                else:
                    all_codes = np.vstack((all_codes, cur_codes))
            # conver to boolean
            all_codes = all_codes.astype(np.bool_)
            print 'sample number: {}; encoding time: {}'.format(len(samps), time.time()-startt)
        except Exception as e:
            print('encoding error: '+str(e))
            raise Exception
        return all_codes
        
    # sets are an array of tensors (samps), so the interface is compatible
    def encode_sets(self, sets, input_type=InputDataFormat.IMG_DATA, norm_type=None):
        set_codes = []
        if input_type == InputDataFormat.FILE:
            set_feats = self.prepare_setfns_for_input(sets)
        cnt = 0
        for cur_set in set_feats:
            cur_codes = self.encode_samples(cur_set, -1, InputDataFormat.IMG_DATA, norm_type)
            set_codes.append(cur_codes)
            cnt += 1
            print '{}/{} set encoded. time cost: {}'.format(cnt, len(sets), time.time()-startt)
        return np.asarray(set_codes)
        
class MLHasher(BaseHasher):
    def build_hash_model(self):
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
        # print self.net.keys()
        
        if self.train_params.loss_type == LossType.Triplet:
            # for triplet loss
            self.net['output'] = NonlinearityLayer(self.net[self.model_params.hash_layer_name], nonlinearity=identity)
        if self.train_params.loss_type == LossType.Classification:
            # for classification loss
            self.net['output'] = DenseLayer(self.net[self.model_params.hash_layer_name], num_units=self.model_params.cls_num, nonlinearity=softmax)