'''
predefined network architecture, pretrained model loading
'''

import numpy as np
import theano

import lasagne
from lasagne.layers import InputLayer, DenseLayer, DropoutLayer, FlattenLayer, NonlinearityLayer
from lasagne.layers import NonlinearityLayer
from lasagne.layers import Conv2DLayer as ConvLayer2D
#from lasagne.layers.dnn import Conv2DDNNLayer as ConvLayer
from lasagne.layers import MaxPool2DLayer
from lasagne.layers.pool import Pool2DLayer
from lasagne.layers import LocalResponseNormalization2DLayer as NormLayer
from lasagne.nonlinearities import softmax, rectify, identity, sigmoid
#from lasagne.layers.special import prelu
from lasagne.layers import prelu

from common import ModelType
from base_model import BaseModel


# build models definitions
class ModelFactory():

    # img_sz: rows/height, cols/width
    def build_model(self, model_type, img_sz):
        if model_type == ModelType.IMAGENET_VGG_S:
            return self.build_vgg_s(img_sz)
        if model_type == ModelType.IMAGENET_VGG_S_GRAY:
            return self.build_vgg_s_gray(img_sz)
        if model_type == ModelType.IMAGENET_VGG16:
            return self.build_vgg16()
        if model_type == ModelType.IMAGENET_VGG19:
            return self.build_vgg19()
        if model_type == ModelType.FACE_CASIA:
            return self.build_casia(img_sz)
        if model_type == ModelType.FACE_CASIA_COLOR:
            return self.build_casia_color(img_sz)
        if model_type == ModelType.FACE_CASIA_COLOR_PRELU:
            return self.build_casia_color_prelu(img_sz)
        if model_type == ModelType.FACE_CASIA_HASH_COLOR_PRELU:
            return self.build_casia_hash_color_prelu(img_sz, 512)
        if model_type == ModelType.FACE_CASIA_HASH_COLOR_PRELU_512:
            return self.build_casia_hash_color_prelu(img_sz, 512)
        if model_type == ModelType.FACE_CASIA_HASH_COLOR_PRELU_256:
            return self.build_casia_hash_color_prelu(img_sz, 256)
        if model_type == ModelType.FACE_CASIA_HASH_COLOR_PRELU_1024:
            return self.build_casia_hash_color_prelu(img_sz, 1024)
        if model_type == ModelType.FACE_CASIA_HASH_COLOR_PRELU_128:
            return self.build_casia_hash_color_prelu(img_sz, 128)
        if model_type == ModelType.MNIST:
            return self.build_mnist()
        if model_type == ModelType.CIFAR10:
            return self.build_cifar10()
        if model_type == ModelType.FACE_VGG:
            return self.build_face_vgg()
        if model_type == ModelType.CIFAR10_NIN:
            return self.build_cifar10_nin()
        if model_type == ModelType.GOOGLENET:
            return self.build_googlenet()

    # oxford vgg deep face model
    def build_face_vgg(self):
        net = {}
        net['input'] = InputLayer((None, 3, 224, 224))
        net['conv1_1'] = ConvLayer2D(net['input'], num_filters=64, filter_size=3, pad=1, nonlinearity=None)
        net['relu1_1'] = NonlinearityLayer(net['conv1_1'], nonlinearity=rectify)
        net['conv1_2'] = ConvLayer2D(net['relu1_1'], num_filters=64, filter_size=3, pad=1, nonlinearity=rectify)
        net['pool1'] = PoolLayer(net['conv1_2'], pool_size=2, stride=2, mode='max', ignore_border=False)
        net['pool1'] = MaxPoolLayer(net['conv1_2'], pool_size=2, stride=2, ignore_border=False) # PoolLayer means MaxPool here...
        net['conv2_1'] = ConvLayer2D(net['pool1'], num_filters=128, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv2_2'] = ConvLayer2D(net['conv2_1'], num_filters=128, filter_size=3, pad=1, nonlinearity=rectify)
        net['pool2'] = Pool2DLayer(net['conv2_2'], pool_size=2, stride=2, mode='max', ignore_border=False)
        net['pool2'] = MaxPool2DLayer(net['conv2_2'], pool_size=2, stride=2, ignore_border=False)
        net['conv3_1'] = ConvLayer2D(net['pool2'], num_filters=256, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv3_2'] = ConvLayer2D(net['conv3_1'], num_filters=256, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv3_3'] = ConvLayer2D(net['conv3_2'], num_filters=256, filter_size=3, pad=1, nonlinearity=rectify)
        net['pool3'] = Pool2DLayer(net['conv3_3'], pool_size=2, stride=2, mode='max', ignore_border=False)
        net['pool3'] = MaxPool2DLayer(net['conv3_3'], pool_size=2, stride=2, ignore_border=False)
        net['conv4_1'] = ConvLayer2D(net['pool3'], num_filters=512, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv4_2'] = ConvLayer2D(net['conv4_1'], num_filters=512, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv4_3'] = ConvLayer2D(net['conv4_2'], num_filters=512, filter_size=3, pad=1, nonlinearity=rectify)
        net['pool4'] = Pool2DLayer(net['conv4_3'], pool_size=2, stride=2, mode='max', ignore_border=False)
        net['pool4'] = MaxPool2DLayer(net['conv4_3'], pool_size=2, stride=2, ignore_border=False)
        net['conv5_1'] = ConvLayer2D(net['pool4'], num_filters=512, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv5_2'] = ConvLayer2D(net['conv5_1'], num_filters=512, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv5_3'] = ConvLayer2D(net['conv5_2'], num_filters=512, filter_size=3, pad=1, nonlinearity=rectify)
        net['pool5'] = Pool2DLayer(net['conv5_3'], pool_size=2, stride=2, mode='max', ignore_border=False)
        net['pool5'] = MaxPool2DLayer(net['conv5_3'], pool_size=2, stride=2, ignore_border=False)
        net['fc6'] = DenseLayer(net['pool5'], num_units=4096, nonlinearity=rectify)
        net['drop6'] = DropoutLayer(net['fc6'], p=0.5)
        net['fc7'] = DenseLayer(net['drop6'], num_units=4096, nonlinearity=rectify)
        net['drop7'] = DropoutLayer(net['fc7'], p=0.5)
        net['fc8'] = DenseLayer(net['drop7'], num_units=2622, nonlinearity=None)
        net['prob'] = lasagne.layers.NonlinearityLayer(net['fc8'], nonlinearity=softmax)
        net['output'] = lasagne.layers.NonlinearityLayer(net['prob'], nonlinearity=identity)
        return net

    # 'learning face recognition from stratch'
    def build_casia(self, img_sz):
        net = {}
        net['input'] = InputLayer((None, 1, img_sz[0], img_sz[1]))
        net['conv11'] = ConvLayer2D(net['input'], num_filters=32, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv12'] = ConvLayer2D(net['conv11'], num_filters=64, filter_size=3, pad=1, nonlinearity=rectify)
        net['norm1'] = NormLayer(net['conv12'], n=3, k=1, beta=0.75, alpha=0.0001)
        net['pool1'] = MaxPool2DLayer(net['norm1'], pool_size=2, stride=2, ignore_border=False)
        net['conv21'] = ConvLayer2D(net['pool1'], num_filters=64, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv22'] = ConvLayer2D(net['conv21'], num_filters=128, filter_size=3, pad=1, nonlinearity=rectify)
        net['norm2'] = NormLayer(net['conv22'], n=3, k=1, beta=0.75, alpha=0.0001)
        net['pool2'] = MaxPool2DLayer(net['norm2'], pool_size=2, stride=2, ignore_border=False)
        net['conv31'] = ConvLayer2D(net['pool2'], num_filters=96, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv32'] = ConvLayer2D(net['conv31'], num_filters=192, filter_size=3, pad=1, nonlinearity=rectify)
        net['pool3'] = MaxPool2DLayer(net['conv32'], pool_size=2, stride=2, ignore_border=False)
        net['conv41'] = ConvLayer2D(net['pool3'], num_filters=128, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv42'] = ConvLayer2D(net['conv41'], num_filters=256, filter_size=3, pad=1, nonlinearity=rectify)
        net['pool4'] = MaxPool2DLayer(net['conv42'], pool_size=2, stride=2, ignore_border=False)
        net['conv51'] = ConvLayer2D(net['pool4'], num_filters=160, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv52'] = ConvLayer2D(net['conv51'], num_filters=320, filter_size=3, pad=1, nonlinearity=None)
        net['pool5'] = Pool2DLayer(net['conv52'], pool_size=7, stride=1, mode='average_inc_pad', ignore_border=False) # or average_exc_pad?
        net['drop5'] = DropoutLayer(net['pool5'], p=0.4)
        #net['fc6'] = DenseLayer(net['drop5'], num_units=10549, nonlinearity=None)
        return net
    
    def build_casia_color(self, img_sz):
        if img_sz is None:
            img_sz = (100, 100)
        net = {}
        net['input'] = InputLayer((None, 3, img_sz[0], img_sz[1]))  # 100x100
        net['conv11'] = ConvLayer2D(net['input'], num_filters=32, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv12'] = ConvLayer2D(net['conv11'], num_filters=64, filter_size=3, pad=1, nonlinearity=rectify)
        net['norm1'] = NormLayer(net['conv12'], n=3, k=1, beta=0.75, alpha=0.0001)
        net['pool1'] = MaxPool2DLayer(net['norm1'], pool_size=2, stride=2, ignore_border=False)
        net['conv21'] = ConvLayer2D(net['pool1'], num_filters=64, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv22'] = ConvLayer2D(net['conv21'], num_filters=128, filter_size=3, pad=1, nonlinearity=rectify)
        net['norm2'] = NormLayer(net['conv22'], n=3, k=1, beta=0.75, alpha=0.0001)
        net['pool2'] = MaxPool2DLayer(net['norm2'], pool_size=2, stride=2, ignore_border=False)
        net['conv31'] = ConvLayer2D(net['pool2'], num_filters=96, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv32'] = ConvLayer2D(net['conv31'], num_filters=192, filter_size=3, pad=1, nonlinearity=rectify)
        net['pool3'] = MaxPool2DLayer(net['conv32'], pool_size=2, stride=2, ignore_border=False)
        net['conv41'] = ConvLayer2D(net['pool3'], num_filters=128, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv42'] = ConvLayer2D(net['conv41'], num_filters=256, filter_size=3, pad=1, nonlinearity=rectify)
        net['pool4'] = MaxPool2DLayer(net['conv42'], pool_size=2, stride=2, ignore_border=False)
        net['conv51'] = ConvLayer2D(net['pool4'], num_filters=160, filter_size=3, pad=1, nonlinearity=rectify)
        net['conv52'] = ConvLayer2D(net['conv51'], num_filters=320, filter_size=3, pad=1, nonlinearity=None)
        net['pool5'] = Pool2DLayer(net['conv52'], pool_size=7, stride=1, mode='average_inc_pad', ignore_border=False) # or average_exc_pad?
        net['drop5'] = DropoutLayer(net['pool5'], p=0.4)
        #net['fc6'] = DenseLayer(net['drop5'], num_units=10549, nonlinearity=None)
        return net
    
    def build_casia_color_prelu(self, img_sz):
        if img_sz is None:
            img_sz = (100, 100)
        net = {}
        default_slope = 0.25 # 0.25 seems to be the default value in caffe
        slope_type = theano.config.floatX
        #print("slope_type: {}".format(type(default_slope)))
        net['input'] = InputLayer((None, 3, img_sz[0], img_sz[1]))
        net['conv11'] = ConvLayer2D(net['input'], num_filters=32, filter_size=3, pad=1, nonlinearity=None)
        net['prelu11'] = prelu(net['conv11'], alpha=np.asarray([default_slope]*32).astype(slope_type))
        net['conv12'] = ConvLayer2D(net['prelu11'], num_filters=64, filter_size=3, pad=1, nonlinearity=None)
        net['prelu12'] = prelu(net['conv12'], alpha=np.asarray([default_slope]*64).astype(slope_type))
        net['norm1'] = NormLayer(net['prelu12'], n=3, k=1, beta=0.75, alpha=0.0001)
        net['pool1'] = MaxPool2DLayer(net['norm1'], pool_size=2, stride=2, ignore_border=False)
        net['conv21'] = ConvLayer2D(net['pool1'], num_filters=64, filter_size=3, pad=1, nonlinearity=None)
        net['prelu21'] = prelu(net['conv21'], alpha=np.asarray([default_slope]*64).astype(slope_type))
        net['conv22'] = ConvLayer2D(net['prelu21'], num_filters=128, filter_size=3, pad=1, nonlinearity=None)
        net['prelu22'] = prelu(net['conv22'], alpha=np.asarray([default_slope]*128).astype(slope_type))
        net['norm2'] = NormLayer(net['prelu22'], n=3, k=1, beta=0.75, alpha=0.0001)
        net['pool2'] = MaxPool2DLayer(net['norm2'], pool_size=2, stride=2, ignore_border=False)
        net['conv31'] = ConvLayer2D(net['pool2'], num_filters=96, filter_size=3, pad=1, nonlinearity=None)
        net['prelu31'] = prelu(net['conv31'], alpha=np.asarray([default_slope]*96).astype(slope_type))
        net['conv32'] = ConvLayer2D(net['prelu31'], num_filters=192, filter_size=3, pad=1, nonlinearity=None)
        net['prelu32'] = prelu(net['conv32'], alpha=np.asarray([default_slope]*192).astype(slope_type))
        net['pool3'] = MaxPool2DLayer(net['prelu32'], pool_size=2, stride=2, ignore_border=False)
        net['conv41'] = ConvLayer2D(net['pool3'], num_filters=128, filter_size=3, pad=1, nonlinearity=None)
        net['prelu41'] = prelu(net['conv41'], alpha=np.asarray([default_slope]*128).astype(slope_type))
        net['conv42'] = ConvLayer2D(net['prelu41'], num_filters=256, filter_size=3, pad=1, nonlinearity=None)
        net['prelu42'] = prelu(net['conv42'], alpha=np.asarray([default_slope]*256).astype(slope_type))
        net['pool4'] = MaxPool2DLayer(net['prelu42'], pool_size=2, stride=2, ignore_border=False)
        net['conv51'] = ConvLayer2D(net['pool4'], num_filters=160, filter_size=3, pad=1, nonlinearity=None)
        net['prelu51'] = prelu(net['conv51'], alpha=np.asarray([default_slope]*160).astype(slope_type))
        net['conv52'] = ConvLayer2D(net['prelu51'], num_filters=320, filter_size=3, pad=1, nonlinearity=None)
        #net['pool5'] = Pool2DLayer(net['conv52'], pool_size=7, stride=1, mode='average_inc_pad', ignore_border=False) # or average_exc_pad?
        net['pool5'] = Pool2DLayer(net['conv52'], pool_size=7, stride=1, mode='average_inc_pad', ignore_border=True) # or average_exc_pad?
        net['drop5'] = DropoutLayer(net['pool5'], p=0.4)
        #net['fc6'] = DenseLayer(net['drop5'], num_units=10549, nonlinearity=None)
        return net

    def build_casia_hash_color_prelu(self, img_sz, nb_bits=512):
        if img_sz is None:
            img_sz = (100, 100)
        net = {}
        default_slope = 0.25 # 0.25 seems to be the default value in caffe
        #print type(default_slope)
        net['input'] = InputLayer((None, 3, img_sz[0], img_sz[1]))
        net['conv11'] = ConvLayer2D(net['input'], num_filters=32, filter_size=3, pad=1, nonlinearity=None)
        net['prelu11'] = prelu(net['conv11'], alpha=np.asarray([default_slope]*32).astype(np.float32))
        net['conv12'] = ConvLayer2D(net['prelu11'], num_filters=64, filter_size=3, pad=1, nonlinearity=None)
        net['prelu12'] = prelu(net['conv12'], alpha=np.asarray([default_slope]*64).astype(np.float32))
        net['norm1'] = NormLayer(net['prelu12'], n=3, k=1, beta=0.75, alpha=0.0001)
        net['pool1'] = MaxPool2DLayer(net['norm1'], pool_size=2, stride=2, ignore_border=False)
        net['conv21'] = ConvLayer2D(net['pool1'], num_filters=64, filter_size=3, pad=1, nonlinearity=None)
        net['prelu21'] = prelu(net['conv21'], alpha=np.asarray([default_slope]*64).astype(np.float32))
        net['conv22'] = ConvLayer2D(net['prelu21'], num_filters=128, filter_size=3, pad=1, nonlinearity=None)
        net['prelu22'] = prelu(net['conv22'], alpha=np.asarray([default_slope]*128).astype(np.float32))
        net['norm2'] = NormLayer(net['prelu22'], n=3, k=1, beta=0.75, alpha=0.0001)
        net['pool2'] = MaxPool2DLayer(net['norm2'], pool_size=2, stride=2, ignore_border=False)
        net['conv31'] = ConvLayer2D(net['pool2'], num_filters=96, filter_size=3, pad=1, nonlinearity=None)
        net['prelu31'] = prelu(net['conv31'], alpha=np.asarray([default_slope]*96).astype(np.float32))
        net['conv32'] = ConvLayer2D(net['prelu31'], num_filters=192, filter_size=3, pad=1, nonlinearity=None)
        net['prelu32'] = prelu(net['conv32'], alpha=np.asarray([default_slope]*192).astype(np.float32))
        net['pool3'] = MaxPool2DLayer(net['prelu32'], pool_size=2, stride=2, ignore_border=False)
        net['conv41'] = ConvLayer2D(net['pool3'], num_filters=128, filter_size=3, pad=1, nonlinearity=None)
        net['prelu41'] = prelu(net['conv41'], alpha=np.asarray([default_slope]*128).astype(np.float32))
        net['conv42'] = ConvLayer2D(net['prelu41'], num_filters=256, filter_size=3, pad=1, nonlinearity=None)
        net['prelu42'] = prelu(net['conv42'], alpha=np.asarray([default_slope]*256).astype(np.float32))
        net['pool4'] = MaxPool2DLayer(net['prelu42'], pool_size=2, stride=2, ignore_border=False)
        net['conv51'] = ConvLayer2D(net['pool4'], num_filters=160, filter_size=3, pad=1, nonlinearity=None)
        net['prelu51'] = prelu(net['conv51'], alpha=np.asarray([default_slope]*160).astype(np.float32))
        net['conv52'] = ConvLayer2D(net['prelu51'], num_filters=320, filter_size=3, pad=1, nonlinearity=None)
        net['pool5'] = Pool2DLayer(net['conv52'], pool_size=7, stride=1, mode='average_inc_pad', ignore_border=False) # or average_exc_pad?
        net['drop5'] = DropoutLayer(net['pool5'], p=0.4)
        # should we dropout here too?
        net['fc_hash{}'.format(nb_bits)] = DenseLayer(net['drop5'], num_units=nb_bits, nonlinearity=sigmoid)
        #net['sig_hash512'] # use a different layer or just nonlinearity?
        #net['fc6'] = DenseLayer(net['hash'], num_units=10549, nonlinearity=None)
        return net

    def build_mnist(self):
        net = {}
        net['input'] = InputLayer(shape=(None, 1, 28, 28))
        net['conv1'] = ConvLayer2D(net['input'], num_filters=32, filter_size=(5,5), 
                                 nonlinearity=lasagne.nonlinearities.rectify,
                                 W=lasagne.init.GlorotUniform())
        net['pool1'] = MaxPool2DLayer(net['conv1'], pool_size=(2,2))
        net['conv2'] = ConvLayer2D(net['pool1'], num_filters=32, filter_size=(5,5),
                                 nonlinearity=lasagne.nonlinearities.rectify)
        net['pool2'] = MaxPool2DLayer(net['conv2'], pool_size=(2,2))
        net['dropout3'] = DropoutLayer(net['pool2'], p=.5)
        net['fc3'] = DenseLayer(net['dropout3'], num_units=256, nonlinearity=lasagne.nonlinearities.rectify)
        net['dropout4'] = DropoutLayer(net['fc3'], p=.5)
        net['output'] = DenseLayer(net['dropout4'], num_units=10, nonlinearity=lasagne.nonlinearities.softmax)
        return net

    # refer to caffe definition (originally from Alex)
    def build_cifar10(self):
        net = {}
        net['input'] = InputLayer(shape=(None, 3, 32, 32))
        net['conv1'] = ConvLayer2D(net['input'], num_filters=32, filter_size=(5,5), 
                                 stride=1, pad=2,
                                 nonlinearity=lasagne.nonlinearities.rectify,
                                 W=lasagne.init.GlorotNormal())
        net['pool1'] = MaxPool2DLayer(net['conv1'], pool_size=(3,3), stride=2)
        net['conv2'] = ConvLayer2D(net['pool1'], num_filters=32, filter_size=(5,5),
                                 stride=1, pad=2,
                                 nonlinearity=lasagne.nonlinearities.rectify,
                                 W=lasagne.init.GlorotNormal())
        net['pool2'] = MaxPool2DLayer(net['conv2'], pool_size=(3,3), stride=2)
        net['conv3'] = ConvLayer2D(net['pool2'], num_filters=64, filter_size=(5,5),
                                 stride=1, pad=2,
                                 nonlinearity=lasagne.nonlinearities.rectify,
                                 W=lasagne.init.GlorotNormal())
        net['pool3'] = Pool2DLayer(net['conv3'], pool_size=(3,3), stride=2, mode='average_inc_pad')
        net['dropout3'] = DropoutLayer(net['pool3'], p=.5)
        net['fc4'] = DenseLayer(net['dropout3'], num_units=64, nonlinearity=None)
        net['dropout4'] = DropoutLayer(net['fc4'], p=.5)
        net['output'] = DenseLayer(net['dropout4'], num_units=10, nonlinearity=lasagne.nonlinearities.softmax)
        return net

    def build_cifar10_nin(self):
        net = {}
        net['input'] = InputLayer((None, 3, 32, 32))
        net['conv1'] = ConvLayer2D(net['input'], num_filters=192, filter_size=5, pad=2)
        net['cccp1'] = ConvLayer2D(net['conv1'], num_filters=160, filter_size=1)
        net['cccp2'] = ConvLayer2D(net['cccp1'], num_filters=96, filter_size=1)
        net['pool1'] = MaxPool2DLayer(net['cccp2'], pool_size=3, stride=2, ignore_border=False)
        net['drop3'] = DropoutLayer(net['pool1'], p=0.5)
        net['conv2'] = ConvLayer2D(net['drop3'], num_filters=192, filter_size=5, pad=2)
        net['cccp3'] = ConvLayer2D(net['conv2'], num_filters=192, filter_size=1)
        net['cccp4'] = ConvLayer2D(net['cccp3'], num_filters=192, filter_size=1)
        net['pool2'] = Pool2DLayer(net['cccp4'], pool_size=3,
                                 stride=2, mode='average_exc_pad', ignore_border=False)
        net['drop6'] = DropoutLayer(net['pool2'], p=0.5)
        net['conv3'] = ConvLayer2D(net['drop6'], num_filters=192, filter_size=3, pad=1)
        net['cccp5'] = ConvLayer2D(net['conv3'], num_filters=192, filter_size=1)
        net['cccp6'] = ConvLayer2D(net['cccp5'], num_filters=10, filter_size=1)
        net['pool3'] = Pool2DLayer(net['cccp6'], pool_size=8, mode='average_exc_pad', ignore_border=False)
        net['output'] = FlattenLayer(net['pool3'])
        return net

    def build_vgg_s(self, img_sz):
        if img_sz is None:
            img_sz = (224, 224)
        net = {}
        net['input'] = InputLayer((None, 3, img_sz[0], img_sz[1]))
        net['conv1'] = ConvLayer2D(net['input'],
                                 num_filters=96,
                                 filter_size=7,
                                 stride=2)
        # caffe has alpha = alpha * pool_size
        net['norm1'] = NormLayer(net['conv1'], alpha=0.0001)
        net['pool1'] = MaxPool2DLayer(net['norm1'],
                                 pool_size=3,
                                 stride=3,
                                 ignore_border=False)
        net['conv2'] = ConvLayer2D(net['pool1'], num_filters=256, filter_size=5)
        net['pool2'] = MaxPool2DLayer(net['conv2'],
                                 pool_size=2,
                                 stride=2,
                                 ignore_border=False)
        net['conv3'] = ConvLayer2D(net['pool2'],
                                 num_filters=512,
                                 filter_size=3,
                                 pad=1)
        net['conv4'] = ConvLayer2D(net['conv3'],
                                 num_filters=512,
                                 filter_size=3,
                                 pad=1)
        net['conv5'] = ConvLayer2D(net['conv4'],
                                 num_filters=512,
                                 filter_size=3,
                                 pad=1)
        net['pool5'] = MaxPool2DLayer(net['conv5'],
                                 pool_size=3,
                                 stride=3,
                                 ignore_border=False)
        net['fc6'] = DenseLayer(net['pool5'], num_units=4096)
        net['drop6'] = DropoutLayer(net['fc6'], p=0.5)
        net['fc7'] = DenseLayer(net['drop6'], num_units=4096)
        net['drop7'] = DropoutLayer(net['fc7'], p=0.5)
        net['fc8'] = DenseLayer(net['drop7'], num_units=1000, nonlinearity=None)
        net['output'] = NonlinearityLayer(net['fc8'], softmax)
        return net

    def build_vgg_s_gray(self, img_sz):
        if img_sz is None:
            img_sz = (224, 224)
        net = {}
        net['input'] = InputLayer((None, 1, img_sz[0], img_sz[1]))
        net['conv1'] = ConvLayer2D(net['input'], num_filters=96, filter_size=7, stride=2)
        # caffe has alpha = alpha * pool_size
        net['norm1'] = NormLayer(net['conv1'], alpha=0.0001)
        net['pool1'] = MaxPool2DLayer(net['norm1'], pool_size=3, stride=3, ignore_border=False)
        net['conv2'] = ConvLayer2D(net['pool1'], num_filters=256, filter_size=5)
        net['pool2'] = MaxPool2DLayer(net['conv2'], pool_size=2, stride=2, ignore_border=False)
        net['conv3'] = ConvLayer2D(net['pool2'], num_filters=512, filter_size=3, pad=1)
        net['conv4'] = ConvLayer2D(net['conv3'], num_filters=512, filter_size=3, pad=1)
        net['conv5'] = ConvLayer2D(net['conv4'],num_filters=512, filter_size=3, pad=1)
        net['pool5'] = MaxPool2DLayer(net['conv5'], pool_size=3, stride=3, ignore_border=False)
        net['fc6'] = DenseLayer(net['pool5'], num_units=4096)
        net['drop6'] = DropoutLayer(net['fc6'], p=0.5)
        net['fc7'] = DenseLayer(net['drop6'], num_units=4096)
        net['drop7'] = DropoutLayer(net['fc7'], p=0.5)
        net['fc8'] = DenseLayer(net['drop7'], num_units=1000, nonlinearity=None)
        net['output'] = NonlinearityLayer(net['fc8'], softmax)
        return net

    def build_vgg16(self, img_sz):
        if img_sz is None:
            img_sz = (224, 224)
        net = {}
        net['input'] = InputLayer((None, 3, img_sz[0], img_sz[1]))
        net['conv1_1'] = ConvLayer2D(net['input'], 64, 3, pad=1)
        net['conv1_2'] = ConvLayer2D(net['conv1_1'], 64, 3, pad=1)
        net['pool1'] = MaxPool2DLayer(net['conv1_2'], 2)
        net['conv2_1'] = ConvLayer2D(net['pool1'], 128, 3, pad=1)
        net['conv2_2'] = ConvLayer2D(net['conv2_1'], 128, 3, pad=1)
        net['pool2'] = MaxPool2DLayer(net['conv2_2'], 2)
        net['conv3_1'] = ConvLayer2D(net['pool2'], 256, 3, pad=1)
        net['conv3_2'] = ConvLayer2D(net['conv3_1'], 256, 3, pad=1)
        net['conv3_3'] = ConvLayer2D(net['conv3_2'], 256, 3, pad=1)
        net['pool3'] = MaxPool2DLayer(net['conv3_3'], 2)
        net['conv4_1'] = ConvLayer2D(net['pool3'], 512, 3, pad=1)
        net['conv4_2'] = ConvLayer2D(net['conv4_1'], 512, 3, pad=1)
        net['conv4_3'] = ConvLayer2D(net['conv4_2'], 512, 3, pad=1)
        net['pool4'] = MaxPool2DLayer(net['conv4_3'], 2)
        net['conv5_1'] = ConvLayer2D(net['pool4'], 512, 3, pad=1)
        net['conv5_2'] = ConvLayer2D(net['conv5_1'], 512, 3, pad=1)
        net['conv5_3'] = ConvLayer2D(net['conv5_2'], 512, 3, pad=1)
        net['pool5'] = MaxPool2DLayer(net['conv5_3'], 2)
        net['fc6'] = DenseLayer(net['pool5'], num_units=4096)
        net['fc7'] = DenseLayer(net['fc6'], num_units=4096)
        net['fc8'] = DenseLayer(net['fc7'], num_units=1000, nonlinearity=None)
        net['output'] = NonlinearityLayer(net['fc8'], softmax)
        return net

    def build_vgg19(self, img_sz):
        if img_sz is None:
            img_sz = (224, 224)
        net = {}
        net['input'] = InputLayer((None, 3, img_sz[0], img_sz[1]))
        net['conv1_1'] = ConvLayer2D(net['input'], 64, 3, pad=1)
        net['conv1_2'] = ConvLayer2D(net['conv1_1'], 64, 3, pad=1)
        net['pool1'] = MaxPool2DLayer(net['conv1_2'], 2)
        net['conv2_1'] = ConvLayer2D(net['pool1'], 128, 3, pad=1)
        net['conv2_2'] = ConvLayer2D(net['conv2_1'], 128, 3, pad=1)
        net['pool2'] = MaxPool2DLayer(net['conv2_2'], 2)
        net['conv3_1'] = ConvLayer2D(net['pool2'], 256, 3, pad=1)
        net['conv3_2'] = ConvLayer2D(net['conv3_1'], 256, 3, pad=1)
        net['conv3_3'] = ConvLayer2D(net['conv3_2'], 256, 3, pad=1)
        net['conv3_4'] = ConvLayer2D(net['conv3_3'], 256, 3, pad=1)
        net['pool3'] = MaxPool2DLayer(net['conv3_4'], 2)
        net['conv4_1'] = ConvLayer2D(net['pool3'], 512, 3, pad=1)
        net['conv4_2'] = ConvLayer2D(net['conv4_1'], 512, 3, pad=1)
        net['conv4_3'] = ConvLayer2D(net['conv4_2'], 512, 3, pad=1)
        net['conv4_4'] = ConvLayer2D(net['conv4_3'], 512, 3, pad=1)
        net['pool4'] = MaxPool2DLayer(net['conv4_4'], 2)
        net['conv5_1'] = ConvLayer2D(net['pool4'], 512, 3, pad=1)
        net['conv5_2'] = ConvLayer2D(net['conv5_1'], 512, 3, pad=1)
        net['conv5_3'] = ConvLayer2D(net['conv5_2'], 512, 3, pad=1)
        net['conv5_4'] = ConvLayer2D(net['conv5_3'], 512, 3, pad=1)
        net['pool5'] = MaxPool2DLayer(net['conv5_4'], 2)
        net['fc6'] = DenseLayer(net['pool5'], num_units=4096)
        net['fc7'] = DenseLayer(net['fc6'], num_units=4096)
        net['fc8'] = DenseLayer(net['fc7'], num_units=1000, nonlinearity=None)
        net['output'] = NonlinearityLayer(net['fc8'], softmax)
        return net
        
    def build_googlenet(self):
        raise NotImplementedError('googlenet has not been defined')

