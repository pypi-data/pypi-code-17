''' 
definition of basic things for deep model learning 

'''

import cPickle as pickle
import numpy as np
import time
import matplotlib.pyplot as plt
import logging

import theano
import lasagne

from common import LossType, InputDataFormat, ModelParamsBase, TrainParamsBase, InputParamsBase, TestParamsBase, ConfigMode
from model_tools import fill_net_from_caffe_protxt
from data_manager import cvimg_to_tensor, load_cv_imgs

# from pretrained_models import create_pretrained_model


'''
 base model to be derived to create custom deep model
 how to train from stratch:
 1) initialize model
 2) build model
 3) train model
 how to finetune a model:
 1) initialize model
 2) build pretrained model and load from file
 3) build new model
 4) train model
'''


class BaseModel(object):
    ''' data '''
    net = {}  # network definition
    class_names = []  # label name for 0~k
    mean_img = None  # average image for normalization

    model_params = ModelParamsBase()
    train_params = TrainParamsBase()
    test_params = TestParamsBase()
    input_params = InputParamsBase()

    iter_funcs = {}  # custom functions for training and testing
    output_func = None  # for extracting output from a specified layer

    ''' 
    training info for vis and logging
    each timestamp contains (iter id, train loss, learning rate etc)
    add it during training
    '''
    train_info = []

    def __init__(self, model_params_, train_params_, input_params_=None, test_params_=None):
        self.model_params = model_params_
        self.train_params = train_params_
        self.input_params = input_params_
        self.test_params = test_params_

    ''' data prepartion '''

    # input NXHXWXC format, modify and output NXCXHXW to feed in network
    def prepare_imgs_for_input(self, cv_imgs):
        return cvimg_to_tensor(cv_imgs)

    # form training data from image files w extra meta info
    def prepare_imgfns_for_input(self, img_fns, extra_info=None):
        print 'base model prepare'
        cv_imgs = load_cv_imgs(img_fns, self.model_params.img_sz)
        return self.prepare_imgs_for_input(cv_imgs)

    ''' model definition '''

    def load_pretrained_model(self):
        pass
        # self.net, self.class_names, self.mean_img = create_pretrained_model(model_type)

    # define custom model
    def build_model(self):
        self.net = {}

    def load_caffe_weights(self, caffe_model_prototxt, caffe_model_path):
        self.net = fill_net_from_caffe_protxt(caffe_model_prototxt, caffe_model_path, self.net)

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
                params = lasagne.layers.get_all_params(self.net[self.model_params.output_layer_name],
                                                       trainable=for_training)
                break
            else:
                cur_layer_params = self.net[layer_name].get_params(trainable=for_training)
                for cur_param in cur_layer_params:
                    params.append(cur_param)
        return params

    # for saving model
    def get_target_param_vals(self):
        param_vals = []
        for layer_name in self.train_params.param_layer_names:
            if layer_name == 'OUTPUT':
                param_vals = lasagne.layers.get_all_param_values(self.net[self.model_params.output_layer_name])
                break
            else:
                cur_layer_params = self.net[layer_name].get_params()
                for cur_param in cur_layer_params:
                    param_vals.append(cur_param.get_value())
        return param_vals

    # for loading model
    def set_target_params(self, param_vals):
        assert len(
            self.train_params.param_layer_names) > 0, 'no parameter layer is specified, set params like this will have random values'
        cnt = 0
        for i in range(len(self.train_params.param_layer_names)):
            if self.train_params.param_layer_names[i] == 'OUTPUT' or (
                    len(self.train_params.param_layer_names) == 1 and len(param_vals) > 2):
                lasagne.layers.set_all_param_values(self.net[self.model_params.output_layer_name], param_vals)
                break
            else:
                cur_layer_params = self.net[layer_name].get_params()
                for cur_param in cur_layer_params:
                    cur_param.set_value(param_vals[cnt])
                    cnt += 1

    # call explicitly before train
    def create_iter_funcs(self, lrate):
        self.iter_funcs['train'] = self.create_iter_train_func(lrate)
        self.iter_funcs['eval'] = self.create_iter_eval_func()

    # define training function
    def create_iter_train_func(self, lrate, th=0.5):
        pass

    # define testing function
    def create_iter_eval_func(self):
        pass

    # train from stratch or fine-tune, return average batch loss
    def learn_model(self, train_data, train_labels, val_data, val_labels, num_epochs):
        pass

    # 　train on large scale data, load by batch
    def learn_model_large_scale(self, train_img_fns, train_labels):
        train_img_fns = np.asarray(train_img_fns)
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
            for id in range(0, len(img_fns) - self.train_params.batch_sz, self.train_params.batch_sz):
                train_batches += 1
                batch_num += 1
                print('processing epoch {} batch {}'.format(epoch, batch_num))
                train_batch_startt = time.time()
                # decrease learning rate after certain iters
                if train_batches % self.train_params.step_lr == 0 and self.train_params.lrate >= 0.0001:
                    self.train_params.lrate *= self.train_params.gamma_lr
                    self.create_iter_funcs(self.train_params.lrate)

                batch_data_prepare_start = time.time()
                cur_batch_fns = img_fns[id:id + self.train_params.batch_sz]
                cur_batch_labels = labels[id:id + self.train_params.batch_sz]
                # print len(cur_batch_fns)
                imgs = self.prepare_imgfns_for_input(cur_batch_fns, self.train_params.extra_input_info)
                if imgs.shape[0] != cur_batch_labels.size:
                    print 'sample and label number not consistent, skip this batch'
                    continue
                print("batch data prepare time: {:.3f}s".format(time.time() - batch_data_prepare_start))
                # print imgs.shape
                # print cur_batch_labels.shape
                train_loss += self.learn_model(imgs, cur_batch_labels, None, None, 1)
                print("total batch time: {:.3f}s".format(time.time() - train_batch_startt))
                print 'epoch {}, batch {} loss: \t\t{:.8f}'.format(epoch + 1, train_batches, train_loss / train_batches)
                if train_loss / train_batches <= self.train_params.stop_loss:
                    break

            if np.mod(epoch, self.train_params.step_save) == 0:
                tmp_fn = self.train_params.model_fn_prefix + '_iter' + str(train_batches) + '.pkl'
                self.save_model(tmp_fn)
            if train_loss / train_batches <= self.train_params.stop_loss:
                break

    ''' model testing '''

    def create_output_func(self, flattern=True):
        if flattern:
            final_layer = lasagne.layers.FlattenLayer(self.net[self.model_params.output_layer_name])
        else:
            final_layer = self.net[self.model_params.output_layer_name]
        output = lasagne.layers.get_output(final_layer, deterministic=True)
        startt = time.time()
        self.output_func = theano.function([self.net['input'].input_var], output)
        print 'output function built. time cost: {}'.format(time.time() - startt)

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
                cur_feat = self.output_func(input_data[i:i + batch_sz])
                if all_feats is None:
                    all_feats = cur_feat
                else:
                    all_feats = np.vstack((all_feats, cur_feat))
                print '{}/{}'.format(len(all_feats), len(input_data))

        print 'compute outputs for {}, time cost: {}'.format(len(input_data), time.time() - startt)
        return all_feats

    ''' model I/O '''

    def save_model(self, save_fn):
        # params = self.get_target_param_vals()
        # should always save all parameters to get complete model
        params = lasagne.layers.get_all_param_values(self.net[self.model_params.output_layer_name])
        data = {}
        data['param_vals'] = params
        data['class_names'] = self.class_names
        data['mean_img'] = self.mean_img
        with open(save_fn, 'wb') as f:
            pickle.dump(data, f)
        print('saved model to {}'.format(save_fn))

    # with default name for corresponding data
    def load_model(self, save_fn,
                   key_names={'class_names': "class_names", "mean_img": "mean_img", "param_vals": "param_vals"}):
        print 'loading model from {}'.format(save_fn)
        startt = time.time()
        data = pickle.load(open(save_fn, 'rb'))
        params = data[key_names['param_vals']]
        # cast to standard type
        for i in range(len(params)):
            params[i] = params[i].astype(np.float32)
        self.class_names = data[key_names['class_names']]
        self.mean_img = data[key_names['mean_img']]
        # try:
        self.set_target_params(params)
        print('model loaded from {}, time cost: {}'.format(save_fn, time.time() - startt))
        # except:
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
        # plt.show()
        if to_save:
            plt.savefig(save_fn)

    def log_train_info(self, save_fn='train_info.log'):
        # this gives IOError: [Errno 27] File too large...
        logging.basicConfig(filename=save_fn, level=logging.INFO)
        for item in self.train_info:
            logging.info('batch {}, learning rate: {}, train loss: {}'.format(item[0], item[2], item[1]))


class ExptConfigBase():
    model_params = ModelParamsBase()
    train_params = TrainParamsBase()
    test_params = TestParamsBase()
    input_params = InputParamsBase()

    ''' task '''
    db_name = ''
    # loss should be in train_params
    loss_name = 'clf'
    # data_format should be in input_params
    # 0: file; 1: image data
    data_format = InputDataFormat.FILE
    # 0: train; 1: test
    mode = ConfigMode.TRAIN
    ''' extra params '''
    #extra_input_info ?
    # are these even used?
    extra_info = ''
    extra_params = {}

    # form model filename
    def fill_params(self):
        pass


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
    model = BaseModel(None, None)

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
    # train_data, train_labels, test_data, test_labels = load_cifar10('E:/Projects/Github/deeplearning/Data/cifar-10-python/')

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
