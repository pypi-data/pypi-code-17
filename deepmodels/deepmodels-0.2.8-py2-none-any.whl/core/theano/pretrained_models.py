''' this script is used to build various pretrained model for lasagne '''

import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle
import io
import skimage.transform
import urllib

import lasagne
from lasagne.layers import InputLayer, DenseLayer, DropoutLayer
from lasagne.layers import Conv2DLayer as ConvLayer
#from lasagne.layers.dnn import Conv2DDNNLayer as ConvLayer
from lasagne.layers import MaxPool2DLayer as PoolLayer
from lasagne.layers import LocalResponseNormalization2DLayer as NormLayer
from lasagne.utils import floatX

from common import ModelType
from model_factory import ModelFactory
import model_tools
from base_model import BaseModel, ModelParamsBase, TrainParamsBase
from data_manager import *


def create_pretrained_model(model_type):
    abspath = os.path.abspath(__file__)
    model_root = os.path.dirname(abspath) + '/../models/'
    model = None
    class_names = None
    mean_image = None
    # use default image size
    model = ModelFactory.build_model(model_type, None)
    if model_type == ModelType.GOOGLENET:
        model_name = 'GoogleNet'
        model_url = 'https://s3.amazonaws.com/lasagne/recipes/pretrained/imagenet/blvc_googlenet.pkl'
        model_fn = model_root + 'blvc_googlenet.pkl'
        # set data
        model_params = pickle.load(open(model_fn, 'rb'))
        class_names = model_params['synset words']
        mean_image = model_params['mean image']
        lasagne.layers.set_all_param_values(model, model_params['values'])
        
        
    if model_type == ModelType.FACE_CASIA_COLOR:
        model_name = 'casia_color'
        model_url = ''
        model_fn = model_root + 'casia_bgr.pickle'
        model_params = pickle.load(open(model_fn, 'rb'))
        class_names = model_params['class_names']
        mean_image = model_params['mean_img']
        lasagne.layers.set_all_param_values(model['drop5'], model_params['param_vals'])
        
    return (model, class_names, mean_image)
        
        
class VGGS(BaseModel):
    model_name = 'VGG-S'
    model_url = 'https://s3.amazonaws.com/lasagne/recipes/pretrained/imagenet/vgg_cnn_s.pkl'
        
    def load_pretrained_model(self):
        abspath = os.path.abspath(__file__)
        model_root = os.path.dirname(abspath) + '/../models/'
        model_fn = model_root + 'vgg_cnn_s.pkl'     
        if os.path.exists(model_fn) is False:
            urllib.urlretrieve(model_url, model_fn)
        
        self.net = ModelFactory().build_model(ModelType.IMAGENET_VGG_S, None)
        self.model_params.output_layer_name = 'output'
        self.load_model(model_fn, {'class_names': 'synset words', 'mean_img': 'mean image', 'param_vals': 'values'})
        # convert mean image (3xhxw) to cvimg format
        self.mean_img = np.transpose(self.mean_img, (1, 2, 0))
        
    def prepare_imgs_for_input(self, imgs, extra_info=None):
        # resize images
        if imgs.shape[1] != self.model_params.img_sz[0] or imgs.shape[2] != self.model_params.img_sz[1]:
            new_imgs = []
            for i in range(len(imgs)):
                cur_img = cv2.resize(imgs[i], self.model_params.img_sz)
                cur_img = cur_img.astype(np.float32)
                cur_img -= self.mean_img
                new_imgs.append(cur_img)
            print new_imgs.shape
            imgs = new_imgs
        return cvimg_to_tensor(imgs)
        
    def prepare_imgfns_for_input(self, img_fns, extra_info=None):
        print 'vggs prepare imgs'
        cv_imgs = load_cv_imgs(img_fns, None)
        new_imgs = []
        for i in range(len(cv_imgs)):
            # resize image to have small dim as 256
            h = cv_imgs[i].shape[0]
            w = cv_imgs[i].shape[1]
            if h > w:
                new_sz = (256, h * 256 / w) # (w,h)
            else:
                new_sz = (w * 256 / h, 256)
            # update size
            w, h = new_sz
            cur_img = cv2.resize(cv_imgs[i], new_sz)
            cur_img = cur_img.astype(np.float32)
            # center crop (224, 224)
            cur_img = cur_img[h / 2 - 112:h / 2 + 112, w / 2 - 112:w / 2 + 112, :]
            # convert to bgr, done
            # subtract mean
            cur_img -= self.mean_img
            new_imgs.append(cur_img)
        
        return self.prepare_imgs_for_input(np.asarray(new_imgs))
    
class VGG16(BaseModel):
    model_name = 'VGG16'
    model_url = 'https://s3.amazonaws.com/lasagne/recipes/pretrained/imagenet/vgg16.pkl'
    
    def load_pretrained_model(self):
        abspath = os.path.abspath(__file__)
        model_root = os.path.dirname(abspath) + '/../models/'
        model_fn = model_root + 'vgg16.pkl'
        if os.path.exists(model_fn) is False:
            urllib.urlretrieve(model_url, model_fn)
        
        self.net = ModelFactory().build_model(ModelType.IMAGENET_VGG16, None)
        self.model_params.output_layer_name = 'output'
        self.load_model(model_fn, {'class_names': 'synset words', 'mean_img': 'mean image', 'param_vals': 'param values'})
        # mean_img is [b, g, r]
        
    def prepare_imgfns_for_input(self, img_fns, extra_info=None):
        startt = time.time()
        cv_imgs = load_cv_imgs(img_fns, None)
        new_imgs = []
        for i in range(len(cv_imgs)):
            # resize image to have small dim as 256
            h = cv_imgs[i].shape[0]
            w = cv_imgs[i].shape[1]
            if h > w:
                new_sz = (256, h * 256 / w) # (w,h)
            else:
                new_sz = (w * 256 / h, 256)
            # update size
            w, h = new_sz
            cur_img = cv2.resize(cv_imgs[i], new_sz)
            cur_img = cur_img.astype(np.float32)
            # center crop (224, 224)
            cur_img = cur_img[h / 2 - 112:h / 2 + 112, w / 2 - 112:w / 2 + 112, :]
            # convert to bgr, done
            # subtract mean
            for j in range(3):
                cur_img[:,:,j] -= self.mean_img[j]

            new_imgs.append(cur_img)

        assert len(new_imgs) > 0, 'empty input images'
        print 'prepare time: {}'.format(time.time() - startt)
        return self.prepare_imgs_for_input(np.asarray(new_imgs))

        
class VGG19(BaseModel):
    model_name = 'VGG19'
    model_url = 'https://s3.amazonaws.com/lasagne/recipes/pretrained/imagenet/vgg19.pkl'
    
    def load_pretrained_model(self):
        abspath = os.path.abspath(__file__)
        model_root = os.path.dirname(abspath) + '/../models/'
        model_fn = model_root + 'vgg19.pkl'
        if os.path.exists(model_fn) is False:
            urllib.urlretrieve(model_url, model_fn)
            
        self.net = ModelFactory().build_model(ModelType.IMAGENET_VGG19, None)
        self.model_params.output_layer_name = 'output'
        self.load_model(model_fn, {'class_names': 'synset words', 'mean_img': 'mean value', 'param_vals': 'param values'})
        
    def prepare_imgfns_for_input(self, img_fns, extra_info=None):
        pass

class CASIA_COLOR(BaseModel):
    model_name = 'casia_color'
    
    def load_pretrained_model(self):
        abspath = os.path.abspath(__file__)
        model_root = os.path.dirname(abspath) + '/../models/face/'
        model_fn = model_root + 'casia_bgr.pickle'
        
        self.net = ModelFactory().build_model(ModelType.FACE_CASIA_COLOR, None)
        old_output = self.model_params.output_layer_name
        self.model_params.output_layer_name = 'drop5'
        self.load_model(model_fn)
        self.model_params.output_layer_name = old_output
        
class CASIA_COLOR_PRELU(BaseModel):
    model_name = 'caisa_color_prelu'
    
    def load_pretrained_model(self):
        abspath = os.path.abspath(__file__)
        model_root = os.path.dirname(abspath) + '/../models/face/'
        model_fn = model_root + 'casia_prelu5M.pickle'
        mean_img_fn = model_root + 'mean_100x100_3c.npy'
        caffe_proto_fn = model_root + 'CASIA_randomcrop_pReLU_rgb_deploy.prototxt'
        caffe_model_fn = model_root + 'casia_randomcrop_prelu_rgb_newproto_iter_5000000.caffemodel'
        
        self.net = ModelFactory().build_model(ModelType.FACE_CASIA_COLOR_PRELU, None)
        old_output_layer = self.model_params.output_layer_name
        self.model_params.output_layer_name = 'drop5'
        if os.path.exists(model_fn) is False:
            self.load_caffe_weights(caffe_proto_fn, caffe_model_fn)
            self.save_model(model_fn)
        else:
            self.load_model(model_fn)
        # load mean image
        self.mean_img = np.load(mean_img_fn)
        self.mean_img = np.transpose(self.mean_img, (1, 2, 0))
        #print self.mean_img.shape
        self.model_params.output_layer_name = old_output_layer

    def prepare_imgfns_for_input(self, img_fns, extra_info=None):
        #print 'casia prelu prepare'
        scale_factor = 0.00390625
        # load raw images
        # JPEG images seems to be decoded differently than in MATLAB, and probably
        # than in Caffe during training...
        imgs = load_cv_imgs(img_fns, None, True)
        # Same problem, also need to double check RGB and orientation in scipy
        # version.
        #imgs = load_scipy_imgs(img_fns, model_params.img_sz, True)
        imgs = imgs.astype(np.float32)
        #print("Preparing images casia new.")

        nb_repeat = 1
        if self.model_params.flip_image:
            nb_repeat*=2
        if self.model_params.crops_image:
            if model_params.crops_image_nb > 0:
                nb_repeat*=model_params.crops_image_nb

        if nb_repeat == 1:
            new_imgs = []
            for i in range(imgs.shape[0]):
                imgh = imgs[i].shape[0]
                imgw = imgs[i].shape[1]
                # center crop 100x100
                new_img = imgs[i, imgh/2-50:imgh/2+50, imgw/2-50:imgw/2+50, :]
                # transpose to rotate
                new_img = np.swapaxes(new_img, 0, 1)
                # subtract mean
                #print new_img.shape
                #print self.mean_img.shape
                new_img -= self.mean_img
                # normalize to 0-1
                new_img *= scale_factor
                #print np.max(new_img)
                new_imgs.append(new_img)
            imgs = new_imgs
        else:
            out_imgs = np.repeat(imgs,nb_repeat,axis=0)
            for i in range(imgs.shape[0]):
                out_range = range(i * nb_repeat,(i + 1) * nb_repeat)
                # transpose to rotate
                out_imgs[out_range] = np.swapaxes(imgs[i], 0, 1)
                # normalize to 0-1
                out_imgs[out_range] *= scale_factor
                if model_params.flip_image:
                    out_imgs[out_range[1::2]] = out_imgs[out_range[1::2],::-1,:,:]
                #if model_params.crops_image:
                # a bit more complicated...
                # subtract mean
                out_imgs[out_range] -= mean_img
            imgs = out_imgs
        # convert to cnn format
        return cvimg_to_tensor(imgs)

class CASIA_HASH_COLOR_PRELU(BaseModel):
    model_name = 'caisa_hash_color_prelu'

    def load_pretrained_model(self):
        abspath = os.path.abspath(__file__)
        model_root = os.path.dirname(abspath) + '/../models/face/'
        model_fn = model_root + 'CASIA_hash512_randomcrop_pReLU_2M.pickle'
        mean_img_fn = model_root + 'mean_100x100_3c.npy'
        caffe_proto_fn = model_root + 'CASIA_hash512_randomcrop_pReLU_deploy.prototxt'
        caffe_model_fn = model_root + 'CASIA_hash512_randomcrop_pReLU_2M.caffemodel'

        self.net = ModelFactory().build_model(ModelType.FACE_CASIA_HASH_COLOR_PRELU, None)
        old_output_layer = self.model_params.output_layer_name
        self.model_params.output_layer_name = 'fc_hash512'
        if os.path.exists(model_fn) is False:
            self.load_caffe_weights(caffe_proto_fn, caffe_model_fn)
            self.save_model(model_fn)
        else:
            self.load_model(model_fn)
        # load mean image
        self.mean_img = np.load(mean_img_fn)
        # transpose mean here ??
        self.mean_img = np.transpose(self.mean_img, (1, 2, 0))
        #print self.mean_img.shape
        self.model_params.output_layer_name = old_output_layer

    def prepare_imgfns_for_input(self, img_fns, extra_info=None):
        print 'casia prelu prepare'
        scale_factor = 0.00390625
        # load raw images
        # JPEG images seems to be decoded differently than in MATLAB, and probably
        # than in Caffe during training...
        imgs = load_cv_imgs(img_fns, None, True)
        # Same problem, also need to double check RGB and orientation in scipy
        # version.
        #imgs = load_scipy_imgs(img_fns, model_params.img_sz, True)
        imgs = imgs.astype(np.float32)
        #print("Preparing images casia new.")

        nb_repeat = 1
        if self.model_params.flip_image:
            nb_repeat*=2
        if self.model_params.crops_image:
            if model_params.crops_image_nb > 0:
                # not yet implemented
                pass
                #nb_repeat*=model_params.crops_image_nb

        if nb_repeat == 1:
            new_imgs = []
            for i in range(imgs.shape[0]):
                imgh = imgs[i].shape[0]
                imgw = imgs[i].shape[1]
                # center crop 100x100
                #new_img = imgs[i, imgh/2-50:imgh/2+50, imgw/2-50:imgw/2+50, :]
                pad = self.model_params.img_sz/2
                new_img = imgs[i, imgh/2-pad[0]:imgh/2+pad[0], imgw/2-pad[1]:imgw/2+pad[1], :]

                # transpose to rotate
                new_img = np.swapaxes(new_img, 0, 1)
                # subtract mean
                print new_img.shape
                print self.mean_img.shape
                new_img -= self.mean_img
                # normalize to 0-1
                new_img *= scale_factor
                print np.max(new_img)
                new_imgs.append(new_img)
            imgs = new_imgs
        else:
            # change that to rely on data_manager augment_img
            print 'beware, using deprecated nb_repeat switch'
            out_imgs = np.repeat(imgs,nb_repeat,axis=0)
            for i in range(imgs.shape[0]):
                out_range = range(i * nb_repeat,(i + 1) * nb_repeat)
                # transpose to rotate
                out_imgs[out_range] = np.swapaxes(imgs[i], 0, 1)
                # normalize to 0-1
                out_imgs[out_range] *= scale_factor
                if model_params.flip_image:
                    out_imgs[out_range[1::2]] = out_imgs[out_range[1::2],::-1,:,:]
                #if model_params.crops_image:
                # a bit more complicated...
                # subtract mean
                out_imgs[out_range] -= mean_img
            imgs = out_imgs
        # convert to cnn format
        return cvimg_to_tensor(imgs)

def test_models(img_fn, model_types):
    print('testing image: ' + img_fn)
    # read image
    img = plt.imread(img_fn)
    model = NetModel()
    # test on each model
    for type in model_types:
        net, class_names, mean_img = create_pretrained_model(type)
        rawimg, newimg = ModelTools.prepare_img_for_test(img, mean_img)
        print newimg.shape
        # predict
        prob = np.array(lasagne.layers.get_output(net['prob'], newimg, deterministic=True).eval())
        top5 = np.argsort(prob[0])[-1:-6:-1]
        # show results
        print('results from: ' + models[type].name)
        for n, label in enumerate(top5):
            print('{}. {}'.format(n+1, class_names[label]))
        #plt.figure()
        #plt.imshow(rawimg.astype('uint8'))
        #plt.axis('off')
        #for n, label in enumerate(top5):
        #    plt.text(250, 70 + n * 20, '{}. {}'.format(n+1, class_names[label]), fontsize=14)


if __name__ == '__main__':
    model_params = ModelParamsBase()
    train_params = TrainParamsBase()
    model = CASIA_HASH_COLOR_PRELU(model_params, train_params)
    model.load_pretrained_model()
    