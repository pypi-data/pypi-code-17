from __future__ import unicode_literals

import os

from glob import glob
from pyspark.sql import Row


def assert_store_keys_exist(temp_dir, timestamp, dataset):
    def fs_keys(path):
        return sorted([y for x in os.walk(path) for y in glob(os.path.join(x[0], '*'))])

    def build_path(path):
        return temp_dir + path.format(timestamp=timestamp.strftime('%Y%m%d%H%M%S%f'), dataset=dataset)
    actual = fs_keys(temp_dir)
    assert build_path('/data') in actual
    assert build_path('/data/{dataset}') in actual
    assert build_path('/data/{dataset}/{timestamp}') in actual
    assert build_path('/data/{dataset}/{timestamp}/_SUCCESS') in actual
    actual_parts = [path for path in actual if path.startswith(build_path('/data/{dataset}/{timestamp}/part-'))]
    assert len(actual_parts) == 1


def to_df(sql_context, data):
    return sql_context._sc\
                      .parallelize(data)\
                      .map(lambda l: Row(**dict(l)))\
                      .toDF()
