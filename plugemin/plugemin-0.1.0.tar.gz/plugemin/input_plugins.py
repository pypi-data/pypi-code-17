import json
import csv
import os

class JsonInput(object):
    def __init__(self, data):
        """JsonInput os a plugemin plugin which parses json and
        yields dicts.

        :param data: An iterator yielding JSON documents, or a filename containing a JSON document per line
        :type data: iterator
        """
        try:
            if os.path.isfile(data):
                with open(data, "r") as fp:
                    data = fp.readlines()
        except TypeError:
            pass
        self.data = data

    def __iter__(self):
        """Iterate through ``self.data`` yielding a dict for each JSON
        document.
        """
        for document in self.data:
            yield json.loads(document)

class CsvInput(object):
    def __init__(self, data):
        """JsonInput os a plugemin plugin which parses json and
        yields dicts.

        :param data: An iterator yielding CSV documents, or a filename containing CSV
        :type data: iterator
        """
        try:
            if os.path.isfile(data):
                with open(data, "r") as fp:
                    data = fp.readlines()
        except TypeError:
            pass
        self.parser = csv.DictReader(data)

    def __iter__(self):
        """Iterate through ``self.data`` yielding a dict for each CSV
        row.
        """
        for row in self.parser:
            yield row
