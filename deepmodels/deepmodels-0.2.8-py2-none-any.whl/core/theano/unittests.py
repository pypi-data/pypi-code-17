import unittest
from data_manager import *
import numpy as np
import os
import cv2
from base_model import *
from deep_clf import DeepClf
from pretrained_models import VGGS, CASIA_COLOR, CASIA_COLOR_PRELU
# from FaceDataManager import *
# from face_hashing import *

'''
testing snnipets
before assembling into large script
'''


''' datamanager testers '''
class DataManagerTester(unittest.TestCase):
    def test_img_convertion(self):
        cv_img = np.zeros((10, 10, 1))
        cv_img = np.reshape(cv_img, (1, cv_img.shape[0], cv_img.shape[1], cv_img.shape[2]))
        print cv_img.shape
        cnn_img = cvimg_to_cnn(cv_img)
        print cnn_img.shape
        self.assertEqual(True, True)

    def test_img_augment(self):
        test_img = cv2.imread('e:\\cat.jpg')
        #cv2.imshow('input', test_img)
        #cv2.waitKey(0)
        #dummy_img = np.zeros((1, 28, 28, 1))
        cnn_img = cvimg_to_cnn([test_img])
        aug_imgs = augment_img(cnn_img, 15, 5, [AugmentType.Crop, AugmentType.Flip, AugmentType.Rotate, AugmentType.ColorShuffle])
        new_imgs = cnn_to_cvimg(aug_imgs)
        for i in range(len(new_imgs)):
            cv2.imwrite('e:\\aug{}.png'.format(i), new_imgs[i])

    def test_triplet_gen(self):
        labels = np.random.randint(3, size=100).tolist()
        triplet_ids = gen_random_triplets(labels, 100)
        # check if consistent
        for triplet in triplet_ids:
            anchor = triplet[0]
            sim_id = triplet[1]
            dis_id = triplet[2]
            print triplet
            self.assertEqual(labels[anchor], labels[sim_id])
            self.assertNotEqual(labels[anchor], labels[dis_id])   
    def test_mean_img(self):
        img_dir = 'E:/Images/'
        img_fns = os.listdir(img_dir)
        img_fns = [os.path.join(img_dir, x) for x in img_fns]
        print 'loaded {} images'.format(len(img_fns))
        mean = compute_mean_img(img_fns, (256,256))
        cv2.imshow('mean', mean)
        cv2.waitKey(0)

''' basedeepmodel testers '''
class DeepModelTester(unittest.TestCase):
    def test_training_plotter(self):
        model = BaseDeepModel(LossType.Classification)
        model.train_info = [(0, 2.4, 1), (0, 2.5, 2), (0, 2.1, 1), (0, 1.8, 9), (0, 1.5, 9)]
        model.draw_train_info()

    def pretrained_models(self):
        class MyModel(CASIA_COLOR_PRELU):
            def build_model(self):
                self.load_pretrained_model()
        model = MyModel(ModelParamsBase(), TrainParamsBase())
        model.build_model()
        imgfns = ['K:/Face/JANUS/CS2/crops_hyperface125x125_target100x100_rgb_tightfb1.6/1/img/3.jpg']
        tensor = model.prepare_imgfns_for_input(imgfns)
        print tensor.shape
        
''' deep clf tester '''

''' deep matcher tester '''

''' data loader '''
class DataLoaderTester(unittest.TestCase):
    def test_ytf_loader(self):
        ytf_root = 'K:/Face/YouTube/YouTubeFaces/'
        ytf_data = load_ytf_from_folders(ytf_root, -1, False, True)
        train_set_fns = ytf_data['train'][0]
        train_set_labels = ytf_data['train'][1]
        train_temp_ids = ytf_data['train'][2]
        train_bbox = ytf_data['train'][3]
        self.assertEqual(train_set_fns.shape[0], train_set_labels.shape[0])
        self.assertEqual(train_set_fns.shape[0], train_temp_ids.shape[0])
        self.assertEqual(train_set_fns.shape[0], train_bbox.shape[0])
        for i in range(train_set_fns.shape[0]):
            self.assertEqual(len(train_set_fns[i]), len(train_bbox[i]))
        test_set_fns = ytf_data['test'][0]
        test_set_labels = ytf_data['test'][1]
        test_temp_ids = ytf_data['test'][2]
        test_bbox = ytf_data['test'][3]
        self.assertEqual(test_set_fns.shape[0], test_set_labels.shape[0])
        self.assertEqual(test_set_fns.shape[0], test_temp_ids.shape[0])
        self.assertEqual(test_set_fns.shape[0], test_bbox.shape[0])
        for i in range(test_set_fns.shape[0]):
            self.assertEqual(len(test_set_fns[i]), len(test_bbox[i]))
        # visualize bbox on random image
        print train_set_fns[13][2]
        img = cv2.imread(train_set_fns[13][2])
        box = train_bbox[13][2]
        print box
        cv2.rectangle(img, (box[0], box[1]), (box[0]+box[2]-1, box[1]+box[3]-1), (0,0,255), 2)
        cv2.imshow('box', img)
        cv2.waitKey(0)

    def test_ijba_loader(self):
        data_dir = 'K:/face/IJBA/'
        data = load_ijba(data_dir, 1, use_set=True)
        with open('./ijba_data.pkl', 'wb') as f:
            pickle.dump(data, f)
        gal_data = data['gal'][0]
        gal_labels = data['gal'][1]
        probe_data = data['probe'][0]
        probe_labels = data['probe'][1]
        print 'gal sample {}, probe sample {}'.format(gal_data.shape[0], probe_data.shape[0])
        self.assertEqual(gal_data.shape[0], gal_labels.shape[0])
        self.assertEqual(probe_data.shape[0], probe_labels.shape[0])

    def test_honda_loader(self):
        data_dir = 'K:/face/Honda/imgs/'
        data = load_honda(data_dir)
        train_data = data['train'][0]
        train_labels = data['train'][1]
        test_data = data['test'][0]
        test_labels = data['test'][1]
        self.assertEqual(train_data.shape[0], train_labels.shape[0])
        self.assertEqual(test_data.shape[0], test_labels.shape[0])

    def test_mnist_loader(self):
        train_data, train_labels, val_data, val_labels, test_data, test_labels = load_mnist(dname + '/../../../Data/mnist.pkl.gz')
        print len(train_data)
        print len(test_data)

    def test_cifar10_loader(self):
        train_data, train_labels, test_data, test_labels = load_cifar10('../../../Data/cifar-10-python/')
        print len(train_data)
        print len(test_data)

''' model conversion '''
class ModelConversionTester(unittest.TestCase):
    # convert casia in caffe to lasagne
    def caffe_casia_tester(self):
        expt_config = DeepPtHashExptConfig()
        expt_config.db_name = 'ytf'
        expt_config.loss_name = 'clf'
        expt_config.model_params.code_len = 128
        expt_config.model_params.img_sz = (100, 100)
        expt_config.data_format = InputDataFormat.FILE
        expt_config.train_params.batch_sz = 32
        expt_config.train_params.loss_type = LossType.Classification
        expt_config.train_params.lrate = 0.01
        expt_config.train_params.model_fn_prefix = \
        'models/{}_set_hash_{}bit_{}_{}'.format(expt_config.db_name, expt_config.model_params.code_dims, expt_config.loss_name, expt_config.extra_info)
        expt_config.train_params.model_fn = expt_config.train_params.model_fn_prefix + '.pkl'
    
        runner = FacePtHashYTFRunner(expt_config)
        runner.build_model()

if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(DeepModelTester("pretrained_models"))
    #suite.addTest(DataManagerTester("test_mean_img"))
    #suite.addTest(DataLoaderTester("test_ijba_loader"))
    #suite.addTest(DataLoaderTester("test_cifar10_loader"))
    runner = unittest.TextTestRunner()
    runner.run(suite)