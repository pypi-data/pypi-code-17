"""

    Model Training
    ~~~~~~~~~~~~~~

    WARNING:

    This script is configured to use
    THEANO as a computational back end.
    To use TensorFlow, make the following
    change:

    K.set_image_dim_ordering('th') --> TO --> K.set_image_dim_ordering('tf')

"""
import sys

training_data_path = "/Users/tariq/Documents/biovida_training_data/biovida_train_val_test"
biovida_path = "/Users/tariq/Google Drive/Programming Projects/BioVida"
sys.path.append(biovida_path)

# General Imports
from keras import backend as K
K.set_image_dim_ordering('th')

from biovida.images.models.image_classification import ImageClassificationCNN


models = ['default', 'squeezenet', '_alex_net']


# ------------------------------------------------------------------------------------------
# Image Classification
# ------------------------------------------------------------------------------------------


def select_model():
    print("The following models can be used:\n")
    for e, m in enumerate(models, start=1):
        print("{0}.".format(str(e)), "'{0}'".format(m.replace("_", " ")))

    model_to_use_no = -1
    while model_to_use_no < 1 or model_to_use_no > len(models):
        model_to_use_no = int(input("Please enter the number of "
                                    "the model you wish to use: "))

    model_to_use = models[model_to_use_no - 1]
    print("Selected Model:", model_to_use)
    return model_to_use


def _image_recognition_cnn_training(epochs, model_to_use, training_data_path, save_name):
    """

    Train the model.

    :param epochs: number of epochs
    :type epochs: ``int``
    :param training_data_path: path to the synthesized_data data
    :type training_data_path: ``str``
    :param save_name: the name of the weights to be saved
    :type save_name: ``str``
    """
    ircnn = ImageClassificationCNN(training_data_path)
    ircnn.convnet(model_to_use=model_to_use)

    ircnn.fit(epochs=epochs)
    ircnn.save(save_name, path='/Users/tariq/Desktop')


save_name = "sq2" #input("Please enter 'save name' for the output file: ")
epochs = 2 #int(input("Please enter the number of epochs: "))
# model_to_use = select_model()
model_to_use = 'default'

_image_recognition_cnn_training(epochs, model_to_use, training_data_path, save_name)


