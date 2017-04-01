'''
library-wise definition
'''

import os

# constant values
# how is this actually use?
core_dir = os.path.dirname(os.path.abspath(__file__))


# types
class InputDataFormat:
    FILE = 0
    IMG_DATA = 1


class CropImage:
    CENTER = 0
    CENTER_4CORNERS = 1
    RANDOM1 = 2


class NormType:
    L1 = 0
    L2 = 1


class ConfigMode:
    TRAIN = 0
    TEST = 1
    FINETUNE = 2


class ModelType:
    IMAGENET_VGG16 = 0
    IMAGENET_VGG19 = 1
    IMAGENET_GNET = 2
    IMAGENET_VGG_S = 3
    IMAGENET_VGG_S_GRAY = 13
    FACE_CASIA = 4
    FACE_CASIA_COLOR = 5
    FACE_CASIA_COLOR_PRELU = 6
    FACE_CASIA_HASH_COLOR_PRELU = 7
    MNIST = 8
    CIFAR10 = 9
    CIFAR100 = 10
    CIFAR10_NIN = 11
    FACE_VGG = 12
    GOOGLENET = 13
    FACE_CASIA_HASH_COLOR_PRELU_512 = 14  # actually same thing as FACE_CASIA_HASH_COLOR_PRELU, but clearer
    FACE_CASIA_HASH_COLOR_PRELU_256 = 15
    FACE_CASIA_HASH_COLOR_PRELU_1024 = 16


class LossType:
    Classification = 0
    Triplet = 1
    TripletClassification = 2
    PairClassification = 3
    TripletImproved = 4


class TripletDist:
    SquaredL2 = 0
    Hamming = 1
    L1 = 2


class TripletType:
    Random = 0
    Hard = 1



class ModelParamsBase:
    ''' Parameters to define the model '''
    model_name = ''
    model_type = ''  # one value from ModelType
    img_sz = (224, 224)
    # classification class number
    cls_num = 10
    # layer for extract output, e.g. feature, prediction etc
    output_layer_name = 'output'


class InputParamsBase:
    ''' Parameters listing how to process inputs '''
    # These are input params that could be used in both train/test
    data_format = InputDataFormat.FILE
    flip_image = False
    crop_image = False
    crop_image_type = CropImage.CENTER


class TrainParamsBase:
    ''' Parameters for training a model '''
    loss_type = LossType.Classification
    loss_name = 'clf'
    lrate = 0.1  # initial learning rate
    step_lr = 10000  # num of batches to reduce learning rate
    gamma_lr = 0.5  # learning rate decay coeff
    step_save = 2  # step/epoch to save model
    num_epochs = 10
    stop_loss = 0.001  # stopping point of loss
    model_fn_prefix = ''  # used for intermedia model save
    model_fn = 'model.pkl'  # final model file
    train_info_log_fn = 'train_info.log'
    batch_sz = 32
    # training data related
    extra_input_info = {}
    # layers to extract parameters
    # if 'OUTPUT' is used, all parameters under output layer will be extracted
    param_layer_names = ['OUTPUT']


class TestParamsBase:
    ''' Parameters for testing a model '''
    model_fn = 'model.pkl'  # model file to load
    test_dataset = None
    batch_encode_sz = 64
    # test data related
    extra_input_info = {}