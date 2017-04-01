'''
deep model for classification
loss is classification loss

'''

import os
import math
import time
import numpy as np
import scipy
from scipy.io import loadmat, savemat
import matplotlib.pyplot as plt
plt.switch_backend('agg')

import theano
import theano.tensor as T
import lasagne

from data_manager import *
from base_model import BaseModel, ExptConfigBase, ExptRunnerBase

curdir = os.path.dirname(os.path.abspath(__file__))
dname = os.path.join(curdir, '../')


class DeepClfExptConfig(ExptConfigBase):
    def fill_params(self):
        self.train_params.model_fn_prefix = \
            '../models/{}_clf_{}'.format(self.db_name, self.extra_info)
        self.train_params.model_fn = self.train_params.model_fn_prefix + '.pkl'

'''
ready to use classification model
'''
# deep classifier
class DeepClf(BaseModel):
    def create_iter_train_func(self, lrate):
        # compute classification loss
        target_var = T.ivector('train_targets')
        train_output = lasagne.layers.get_output(
            self.net[self.model_params.output_layer_name])
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
        return train_fn
        
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
        
    # train model with actual data (not files)
    def learn_model(self, train_data, train_labels, val_data, val_labels, num_epochs):
        print 'training in normal mode'
        if 'train' not in self.iter_funcs:
            self.create_iter_funcs(self.train_params.lrate)
            
        train_data = np.asarray(train_data)
        train_labels = np.asarray(train_labels, np.int32)
        # launch the training loop
        print("Starting training...")
        print('batch size: {}, epochs: {}'.format(self.train_params.batch_sz, num_epochs))
        start_t = time.time()
        total_batches = 0
        total_loss = 0
        # We iterate over epochs:
        for epoch in range(num_epochs):
            # In each epoch, we do a full pass over the training data:
            train_loss = 0
            train_batches = 0
            print 'learning rate: {}'.format(self.train_params.lrate)
            if np.mod(epoch, self.train_params.step_lr)==0 and epoch > 0:
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
        print 'total training time: {}'.format(time.time()-start_t)
        return total_loss / total_batches

    def eval_clf(self, test_data, test_labels):
        eval_fn = self.create_iter_eval_func()
        loss, accu = eval_fn(test_data, test_labels)
        print('classification accuracy: {}'.format(accu))
    def eval_clf_fns(self, test_fns, test_labels, topK):
        # load data
        test_data = self.prepare_imgfns_for_input(test_fns)
        if topK == 1:
            self.eval_clf(test_data, test_labels)
        else:
            probs = self.get_outputs(test_data)
            top_num = min(topK, len(probs[0]))
            top_labels = np.argsort(probs, axis=1)[:, -1:-1-top_num:-1]
            # compute accuracy
            accu = 0;
            for i in range(len(top_labels)):
                if test_labels[i] in top_labels[i]:
                    accu += 1
            print('classification accuracy: {}'.format(accu*1.0/len(test_labels)))
        
    # predict top K image labels
    def predict_img(self, img_fn, topK):
        print('testing image: ' + img_fn)
        # read image
        img_fns = [img_fn]
        input = self.prepare_imgfns_for_input(img_fns)
        # predict
        startt = time.time()
        # np.array(lasagne.layers.get_output(self.net['output'], input, deterministic=True).eval())
        prob = self.get_outputs(input)
        print 'prediction time (without compilation): {}s'.format(time.time()-startt)
        top_num = min(topK, len(prob[0]))
        top_labels = np.argsort(prob[0])[-1:-1-top_num:-1]
        top_prob = np.sort(prob[0])[-1:-1-top_num:-1]
        # show results
        for n, label in enumerate(top_labels):
            print('{}. {}: {}'.format(n+1, self.class_names[label], top_prob[n]))



# common models
class DeepClfGooglenet(DeepClf):
    def load_pretrained_model(self):
        raise NotImplementedError('googlenet not implemented')
        # gnet = modelzoo.googlenet.build_model()
        # model_params = pickle.load(open(models[model_type].model_fn))
        # CLASS = model_params['synset words']
        # MEAN_IMAGE = model_params['mean image']
        
    def build_model(self):
        self.load_pretrained_model()
        
    def prepare_imgfns_for_input(self, img_fns, extra_info=None):
        pass




class DeepObjClfRunner(ExptRunnerBase):
    pass


def run_clf():
    expt_config = ExptConfigBase()
    expt_config.train_params.param_layer_names = ['OUTPUT']
    model = DeepClfVGGS(expt_config.model_params, expt_config.train_params)
    model.build_model()
    imgfns = ['F:/Fashion/EyeStyle/ShopStyle_2016_02/Images/blazers/332351862__a0a112da827b17b9cc149bbd158c704a__p.jpg',
              'e:/images/1_26_26982.jpg']
    model.predict_img(imgfns[0], 30)


if __name__ == '__main__':
    run_clf()
