"""


"""
import numpy as np
from numpy import array
from PIL import Image
from scipy.misc import imresize
from biovida.images import OpeniInterface
from biovida.images import OpeniImageProcessing

from sklearn.metrics import matthews_corrcoef

path = "/Users/tariq/Desktop/test_image.png"


# Model
opi = OpeniInterface()
ip = OpeniImageProcessing(opi, db_to_extract='cache_records_db')
model = ip._ircnn.model
image_shape = ip._ircnn.image_shape

# Test
image = array(Image.open(path))


def image_reformat(image, image_shape=(224, 224)):
    image = imresize(image, image_shape)
    image = image.transpose((2,0,1))
    image = image.astype('float32')
    image = image / 255
    return np.expand_dims(image, axis=0)

x_test = array([image_reformat(image)]*3)
y_test = np.array([1, 0])

out = array(model.predict_proba(x_test[0]))


acc = []
accuracies = []
threshold = np.arange(0.1, 0.9, 0.1)
best_threshold = np.zeros(out.shape[1])
for i in range(out.shape[1]):
    y_prob = np.array(out[:, i])
    for j in threshold:
        y_pred = [1 if prob >= j else 0 for prob in y_prob]
        acc.append(matthews_corrcoef(y_test[:, i], y_pred))
    acc = np.array(acc)
    index = np.where(acc == acc.max())
    accuracies.append(acc.max())
    best_threshold[i] = threshold[index[0][0]]
    acc = []



test_data = "/Users/tariq/Desktop/dataset"

to_location


































