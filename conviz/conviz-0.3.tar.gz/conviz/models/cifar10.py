import os

from keras.models import load_model

from conviz.utils.data_util import DataUtil


def load():
    model_path = DataUtil.load_file(
        os.path.join(DataUtil.get_cache_path(), "models", "cifar10.h5"),
        "http://gdurl.com/mb6h"
    )
    return load_model(model_path)
