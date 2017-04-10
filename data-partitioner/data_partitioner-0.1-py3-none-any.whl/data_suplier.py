"""
Suplies the data to the harness.
"""

from data_partitioner.partitioner import partitioner, pseudorandom_function

class DataSuplier(object):
    """A class that takes a dataset and separtes it into a training set and a test set in a
    conistant manner."""

    def __init__(
            self,
            dataset,
            training_percent=0.8,
            partitioning_function=pseudorandom_function
    ):
        self.dataset = dataset
        self.training_percent = training_percent
        self.n_of_elements = len(dataset)
        self.partitioner = partitioner(
            self.n_of_elements,
            [training_percent, 1-training_percent],
            partitioning_function,
        )
        self.test_indexes = []
        self.training_indexes = []
        self.index = 0

    def test_set(self):
        """Returns the generator for the test set."""
        return self._yield_set(self.test_indexes)

    def training_set(self):
        """Returns the generator for the training set."""
        return self._yield_set(self.training_indexes)

    def _yield_set(self, indexes):
        returned = 0
        while self.index < self.n_of_elements or returned < len(indexes):
            while returned == len(indexes) and self.index < self.n_of_elements:
                self.__next()
            if returned < len(indexes):
                index = indexes[returned]
                yield (index, self.dataset[index])
                returned += 1

    def __next(self):
        res = self.partitioner.__next__()
        if res == 0:
            self.training_indexes.append(self.index)
        else:
            self.test_indexes.append(self.index)
        self.index += 1
        return res
