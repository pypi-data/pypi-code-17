import random
from abc import abstractmethod


class ArgData:

    @abstractmethod
    def set_data(self, amount):
        pass

    @abstractmethod
    def inc_data(self, amount):
        pass

    @abstractmethod
    def get_data_size(self):
        pass

    @abstractmethod
    def get_raw_data(self):
        pass


class ArgDataListImpl(ArgData, list):

    def __init__(self, listt):
        self.listt = listt
        super(ArgDataListImpl, self).__init__(listt)

    def set_data(self, amount):
        self.listt = [random.randint(0, 1000) for _ in range(amount)]

    def inc_data(self, amount):
        extra = [random.randint(0, 1000) for _ in range(amount)]
        self.listt += extra

    def get_data_size(self):
        return len(self.listt)

    def get_raw_data(self):
        return self.listt
