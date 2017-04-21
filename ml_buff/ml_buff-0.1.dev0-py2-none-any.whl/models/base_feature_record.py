from ml_buff.models.base_feature_repository import BaseFeatureRepository
from ml_buff.database import session_scope

class FeatureMeta(type):
    def __init__(cls, name, bases, dct):
        super(FeatureMeta, cls).__init__(name, bases, dct)
        cls._class = cls.__name__

class BaseFeatureRecord(metaclass=FeatureMeta):
    _input_data_values = None

    def __init__(self):
        if (self.getModel() == None):
            with session_scope() as session:
                BaseFeatureRepository().create(session, self._class)

    def getModel(self):
        with session_scope() as session:
            return BaseFeatureRepository().get(session, self._class)

    def getOrCreateModel(self):
        model = self.getModel()
        if model is None:
            with session_scope() as session:
                model = create(self, session, self._class)
        return model

    def setInputDataValues(self, input_data_values):
        self._input_data_values = input_data_values

    def calculate(self, input_data):
        return [0]

    def getValue(self, input_data):
        with session_scope() as session:
            return BaseFeatureRepository().getValue(session, self._class, input_data)

    def getOrCreateValue(self, input_data):
        featureValue = self.getValue(input_data)
        if featureValue is None:
            with session_scope() as session:
                value = self.calculate(input_data)
                BaseFeatureRepository().createValue(session, self._class, input_data, value)

    def createValue(self, input_data):
        with session_scope() as session:
            value = self.calculate(input_data)
            BaseFeatureRepository().createValue(session, self._class, input_data, value)

