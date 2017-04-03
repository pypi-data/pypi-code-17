from setuptools import setup, find_packages
setup(
    name='aws-iot-segmentation',
    packages=find_packages(exclude=['tests']),
    version='0.1',
    description='A library which segments big message to be sent on AWS IOT Broker',
    author='Andrei Mircescu',
    author_email='mircescu.andrei@gmail.com',
    url='https://github.com/andreimircescu/aws-iot-segmentation/archive/0.1.tar.gz',
    download_url='https://github.com/andreimircescu/aws-iot-segmentation/archive/0.1.tar.gz',
    keywords=['AWS', 'IOT', 'message', 'segmentation'],
    classifiers=[],
)
