from distutils.core import setup
import unittest


def get_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(
    name='aws-iot-segmentation',
    packages=['aws_iot_segmentation'],
    version='0.5',
    description='A library which segments big message to be sent on AWS IOT Broker',
    author='Andrei Mircescu',
    author_email='mircescu.andrei@gmail.com',
    url='https://github.com/andreimircescu/aws-iot-segmentation/archive/0.5.tar.gz',
    download_url='https://github.com/andreimircescu/aws-iot-segmentation/archive/0.5.tar.gz',
    keywords=['AWS', 'IOT', 'message', 'segmentation'],
    test_suite="'setup.get_test_suite'",
    classifiers=[],
)
