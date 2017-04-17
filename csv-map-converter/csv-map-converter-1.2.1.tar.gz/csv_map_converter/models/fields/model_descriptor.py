
from .base import FIELD_LIST

class ModelDescriptor():

    def __init__(self, Model):
        self.__field_dict = self.__get_all_dict_of_model_field(Model)

    def get(self, name):
        return self.__field_dict.get(name)

    def __get_all_dict_of_model_field(self, Model):
        field_dict = dict()
            
        for attr_name in dir(Model):
            field = getattr(Model, attr_name)
            if field.__class__ in FIELD_LIST:
                if field.name:
                    field_dict[field.name] = field
                else:
                    field_dict[attr_name] = field
        return field_dict


