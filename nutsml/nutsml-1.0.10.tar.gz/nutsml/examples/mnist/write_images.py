"""
.. module:: write_images
   :synopsis: Example for writing of image data
"""

from nutsflow import Take, Consume, Enumerate, Zip, Format, Get
from nutsml import WriteImage


def load_samples():
    from keras.datasets import mnist
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    return zip(X_train, y_train), zip(X_test, y_test)


if __name__ == '__main__':
    train_samples, _ = load_samples()
    imagepath = 'images/*.png'
    names = Enumerate() >> Zip(train_samples >> Get(1)) >> Format('{1}/img{0}')
    train_samples >> Take(30) >> WriteImage(0, imagepath, names) >> Consume()
